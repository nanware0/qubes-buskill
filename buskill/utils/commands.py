'''
Contains CLI command pathes, so there is no error possible.
'''

# typing imports
from typing import Self, Any, cast

# shutil imports
from shutil import which

class Commands():
    def __init__(self: Self, commands: dict[str, str] | None = None):
        self._commands: dict[str, tuple[str, str]] = {}

        if commands is None:
            commands = {}
            
        for command_name, command in commands.items():
            self.__setattr__(command_name, command)

    def __getattribute__(self: Self, name: str) -> Any:
        if name.startswith('_'):
            try:
                return super().__getattribute__(name)
            except:
                return None
        else:
            if name in self._commands:
                return self._commands[name][1]
            else:
                return '@null'

    def __setattr__(self: Self, name: str, value: Any) -> None:
        if not name.startswith('_'):
            if isinstance(value, str):
                self._commands[name] = (value, which(value) or '')
        else:
            super().__setattr__(name, value)

    def __delattr__(self: Self, name: str) -> None:
        self._commands.pop(name, None)

    def __getitem__(self: Self, key: str) -> str:
        if key.startswith('_'):
            return '@null'
        else:
            return cast(str, self.__getattribute__(key))

    def __setitem__(self: Self, key: str, value: str) -> None:
        self.__setattr__(key, value)

    def __delitem__(self: Self, key: str) -> None:
        self.__delattr__(key)

    def _refresh(self: Self) -> None:
        for command, command_tuple in self._commands.items():
                self._commands[command] = (command_tuple[0], which(command_tuple[0]) or '')

    def _clear(self: Self) -> None:
        self._commands.clear()


COMMANDS: Commands = Commands(
    {
        'CRYPTSETUP': 'cryptsetup',

        'MOUNT': 'mount',
        'LSBLK': 'lsblk',
        'LDD': 'ldd',
        'SYNC': 'sync',

        'ECHO': 'echo',
        'CAT': 'cat',

        'POWEROFF': 'poweroff',
        'SHUTDOWN': 'shutdown',
        'REBOOT': 'reboot',

        'LOGINCTL': 'loginctl',

        'QDBUS': 'qdbus',
        'XFCE4_SCREENSAVER_COMMAND': 'xfce4-screensaver-command',
        'XFLOCK4': 'xflock4',
        'I3LOCK': 'i3lock',
        'SLOCK': 'slock',

        'WPCTL': 'wpctl',

        'BASH': 'bash',
        'SUDO': 'sudo'
    }
)

def refresh_commands() -> None:
    COMMANDS._refresh() # pyright: ignore[reportPrivateUsage]

def clear_commands() -> None:
    COMMANDS._clear() # pyright: ignore[reportPrivateUsage]