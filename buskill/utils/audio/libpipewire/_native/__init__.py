__all__: list[str] = []

from typing import Literal
LIBRARY_NAMES: tuple[Literal['libpipewire-0.3.so.0', 'libpipewire-0.3.so'], ...] = ('libpipewire-0.3.so.0', 'libpipewire-0.3.so')
'''The possible names for libpipewire-0.3'''
__all__ += ['LIBRARY_NAMES']

from .errors import PipeWireError, PipeWireLibraryNotFoundError
__all__ += [
    'PipeWireError',
    'PipeWireLibraryNotFoundError'
]

from .functions import load_cdll, require_handle
__all__ += [
    'load_cdll',
    'require_handle'
]

from .Native import Native
__all__ += ['Native']

from .PipeWireRuntime import PipeWireRuntime
__all__ += ['PipeWireRuntime']