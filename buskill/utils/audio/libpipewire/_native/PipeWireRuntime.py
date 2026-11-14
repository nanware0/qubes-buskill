# typing imports
from typing import ClassVar, Sequence, Self

# types imports
from types import TracebackType

# sys imports
import sys

# buskill imports
from buskill.utils.audio.libpipewire._native import Native
from buskill.utils.audio.libpipewire._native import PipeWireError, load_cdll

class PipeWireRuntime():
    '''Owns the process-wide pw_init/pw_deinit pair. Only one may be active at a time.'''

    _active: ClassVar[bool] = False

    def __init__(self: Self, argv: Sequence[str] | None = None) -> None:
        '''Initialize the pipewire runtime.'''
        self._argv: list[str] = list(argv) if argv is not None else list(sys.argv)
        self._native: Native | None = None

    def __enter__(self: Self) -> Self:
        '''
        Enter the runtime.  
        Load libpipewire and initialize the Native object, then, initialize the PipeWire system.  
        Raise an error if a PipeWireRuntime is already active.
        '''
        if PipeWireRuntime._active:
            raise PipeWireError('a PipeWireRuntime is already active in this process')
        native: Native = Native(load_cdll())
        native.init(self._argv)
        PipeWireRuntime._active = True
        self._native = native
        return self

    def __exit__(
        self: Self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        '''
        Exit/close the runtime.  
        Deinitialize the PipeWire system.
        '''
        if self._native is not None:
            self._native.deinit()
            self._native = None
            PipeWireRuntime._active = False

    @property
    def native(self: Self) -> Native:
        '''Return the Native object. Raise an error if None (so if the runtime isn't entered).'''
        if self._native is None:
            raise PipeWireError('PipeWireRuntime is not entered')
        return self._native