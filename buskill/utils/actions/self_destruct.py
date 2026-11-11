# buskill imports
from buskill.utils import delay_execution, refresh_commands, COMMANDS
from buskill.utils.qubes import kill_qubes
from buskill.utils.actions import lock_screen, shutdown
from buskill.utils.config.manager import CONFIG_MANAGER

# subprocess imports
import subprocess

# json imports
import json

# typing imports
from typing import Any, Literal, cast

# asyncio imports
import asyncio
from asyncio import AbstractEventLoop, Future

# pathlib imports
from pathlib import Path

# shutil imports
import shutil

# re imports
import re

async def self_destruct() -> bool | None:
    '''
    Self-destruct trigger script for BusKill : permanently erase the data of the computer.

    Returns:
        *False* if not authorized, else nothing
    '''

    refresh_commands()
    LSBLK: str = COMMANDS.LSBLK
    SYNC: str = COMMANDS.SYNC
    BASH: str = COMMANDS.BASH
    ECHO: str = COMMANDS.ECHO
    MOUNT: str = COMMANDS.MOUNT
    CRYPTSETUP: str = COMMANDS.CRYPTSETUP
    POWEROFF: str = COMMANDS.POWEROFF
    SHUTDOWN: str = COMMANDS.SHUTDOWN
    CAT: str = COMMANDS.CAT
    LDD: str = COMMANDS.LDD

    if not CONFIG_MANAGER.general.self_destruct_authorized: # Verify if the self destruction is authorized
        return False # Return false if not authorized

    loop: AbstractEventLoop = asyncio.get_event_loop()

    loop.create_task(delay_execution(60, {'func': shutdown, 'args': [True], 'kwargs': {}}))

    loop.run_in_executor(None, lock_screen) # Lock screen immediatly in background

    loop.run_in_executor(None, kill_qubes, ['@all']) # Kill every qube in background to accelerate hard shutdown

    lsblk_json: Any = json.loads(subprocess.run([LSBLK, '--json', '--output', 'UUID,FSTYPE'], capture_output=True, text=True).stdout)

    writes: list[Future[Any]] = []

    for device_dict in lsblk_json.get('blockdevices'):
        try:
            fstype: Any = device_dict.get('fstype')
            uuid: Any = device_dict.get('uuid')
            if isinstance(fstype, str) and isinstance(uuid, str):
                if 'crypt' in fstype:
                    device: str = f'/dev/disk/by-uuid/{uuid}'
                    writes.append(loop.run_in_executor(None, overwrite_luks_keyslots, device))
                    luksVersion: int
                    with open(device, 'rb') as f:
                        f.seek(6)
                        luksVersion = int.from_bytes(f.read(2), byteorder='big')

                    luksEndByte: int

                    if luksVersion == 1:
                        payloadOffset: int
                        with open(device, 'rb') as f:
                            f.seek(104)
                            payloadOffset = int.from_bytes(f.read(4), byteorder='big')
                        luksEndByte = 512 * payloadOffset
                    elif luksVersion == 2:
                        hdr_size: int
                        with open(device, 'rb') as f:
                            f.seek(8)
                            hdr_size = int.from_bytes(f.read(8), byteorder='big')
                        luksEndByte = 2 * hdr_size
                    else:
                        luksEndByte = 20_971_520

                    writes.append(loop.run_in_executor(None, write_random, luksEndByte, device))
        except: pass

    await asyncio.gather(*writes)
    writes.clear()
    subprocess.run([SYNC])
    subprocess.run([BASH, '-c', f'{ECHO} 3 > /proc/sys/vm/drop_caches'])

    CHROOT_PATH: Path = Path('/dev/shm/buskill/chroot')
    for element in ['proc', 'sys', 'dev', 'pts', 'bin', 'lib64', 'lib/systemd', 'usr/sbin', 'usr/bin']:
        (CHROOT_PATH / element).mkdir(parents=True, exist_ok=True)

    subprocess.run([MOUNT, '-t', 'proc', 'none', f'{(CHROOT_PATH / 'proc').as_posix()}'])
    subprocess.run([MOUNT, '-t', 'sysfs', 'none', f'{(CHROOT_PATH / 'sys').as_posix()}'])
    subprocess.run([MOUNT, '-o', 'bind', '/dev', f'{(CHROOT_PATH / 'dev').as_posix()}'])
    subprocess.run([MOUNT, '-o', 'bind', '/dev/pts', f'{(CHROOT_PATH / 'dev/pts').as_posix()}'])

    for binary in [BASH, CRYPTSETUP, ECHO, SYNC, POWEROFF, SHUTDOWN, CAT]:
        shutil.copy(Path(binary), CHROOT_PATH)
        ldd_result: str = subprocess.run([LDD, binary], capture_output=True, text=True).stdout
        pattern: Literal['/lib.*\\.so(\\.[0-9]*)*']
        pattern = r'/lib.*\.so(\.[0-9]*)*'
        
        for lib in re.findall(pattern, ldd_result):
            shutil.copy(Path(lib), CHROOT_PATH)

    shutil.move(CHROOT_PATH / 'lib', CHROOT_PATH / 'usr')
    (CHROOT_PATH / 'lib').symlink_to(CHROOT_PATH / 'usr/lib')

    COMMANDS.CAT = (CHROOT_PATH / CAT).as_posix()
    COMMANDS.BASH = (CHROOT_PATH / BASH).as_posix()
    COMMANDS.POWEROFF = (CHROOT_PATH / POWEROFF).as_posix()
    COMMANDS.SHUTDOWN = (CHROOT_PATH / SHUTDOWN).as_posix()
    

    loop.create_task(
        delay_execution(
            60, 
            {
                'func': shutdown, 
                'args': [True], 
                'kwargs': {}
            }
        )
    )

    for _device in Path('/dev/mapper').iterdir():
        writes.append(loop.run_in_executor(None, subprocess.run, [CRYPTSETUP, 'luksSuspend', _device.resolve().as_posix()]))

    await asyncio.gather(*writes)

    subprocess.run([SYNC])
    subprocess.run([BASH, '-c', f'{ECHO} 3 > /proc/sys/vm/drop_caches'])
    loop.run_in_executor(None, shutdown, True)

def write_random(length: int, file: str) -> None:
    with open('/dev/urandom', 'rb') as urandom:
        with open(file, 'wb') as f:
            remaining: int = length
            while remaining > 0:
                chunk = urandom.read(min(1_048_576, remaining))
                f.write(chunk)
                remaining -= len(chunk)

def overwrite_luks_keyslots(device: str) -> None:
    try:
        subprocess.run([cast(str, COMMANDS.CRYPTSETUP), 'luksErase', '--batch-mode', device], check=True)
    except:
        write_random(20_971_520, device)