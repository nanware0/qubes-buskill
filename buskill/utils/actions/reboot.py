# The package policy is that every step must be commented 
# and that documenting the code is an obligation, 
# don't be afraid by the comments,
# they're here to specify the expected behavior

# buskill imports
from buskill.utils import COMMANDS

# subprocess imports
import subprocess

def reboot(hard: bool) -> None:
    '''
    Reboot the computer.

    :param hard: If set to True, using hard reboot, else, using soft reboot
    '''
    cat: str = COMMANDS.CAT
    bash: str = COMMANDS.BASH
    reboot: str = COMMANDS.POWEROFF
    shutdown: str = COMMANDS.SHUTDOWN

    if hard: # First case : hard reboot
        # Verify if sysrq is totally enabled
        if subprocess.run([cat, '/proc/sys/kernel/sysrq'], capture_output=True, text=True).stdout == '1':
            try:
                subprocess.run([bash, '-c', 'echo b > /proc/sysrq-trigger'], check=True) # Try to hard reboot with sysrq
            except: # In case that didn't work (very unlikely), fallback to other reboot system
                try:
                    subprocess.run([reboot, '-f', '--no-wall'], check=True) # Try to reboot using poweroff, cuting the power of the computer
                except:
                    try:
                        subprocess.run([shutdown, '-r', '--no-wall', 'now'], check=True) # Try to reboot and bypass verifications
                    except:
                        subprocess.run([reboot]) # Fallback to soft reboot
        else:
            try:
                subprocess.run([reboot, '-f', '--no-wall'], check=True) # Try to reboot using poweroff, cuting the power of the computer
            except:
                try:
                    subprocess.run([shutdown, '-r', '--no-wall', 'now'], check=True) # Try to reboot and bypass verifications
                except:
                    subprocess.run([reboot]) # Fallback to soft reboot
    else:
        subprocess.run([reboot]) # Soft reboot