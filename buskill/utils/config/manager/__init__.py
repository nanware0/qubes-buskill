__all__: list[str] = []

from typing import Callable
type ApplyFunc = Callable[[list[str]], None]

from .Manager import Manager
__all__ += ['Manager']

from .Action import ActionManager
__all__ += ['ActionManager']

from .Alarm import AlarmManager
__all__ += ['AlarmManager']

from .General import GeneralManager
__all__ += ['GeneralManager']

from .Recovery import RecoveryManager
__all__ += ['RecoveryManager']

from .System import SystemManager
__all__ += ['SystemManager']

from .Config import CONFIG_MANAGER, ConfigManager
__all__ += ['CONFIG_MANAGER', 'ConfigManager']