'''
NOT FINISHED YET
'''

__all__: list[str] = []

from .objects import Verbose, LogType, Color
__all__ += [
    'Verbose',
    'LogType',
    'Color'
]

from .Logger import Logger
__all__ += ['Logger']