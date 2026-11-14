# buskill imports
from buskill.utils.audio.libpipewire._native import PipeWireRuntime, Native

# types imports
from types import TracebackType

# typing imports
from typing import Self

from buskill.utils.audio.libpipewire._native import PipeWireError

class MainLoop():
    '''A pw_main_loop. Must be created inside an active PipeWireRuntime.'''

    def __init__(self: Self, runtime: PipeWireRuntime) -> None:
        '''Initialize the loop in a specific PipeWireRuntime (runtime).'''
        self._native: Native = runtime.native
        self._handle: int | None = self._native.main_loop_new()

    def __enter__(self: Self) -> Self:
        '''Enter the loop. It just returns itself.'''
        return self

    def __exit__(
        self: Self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        '''Exit the loop (close it).'''
        self.close()

    @property
    def loop_handle(self: Self) -> int:
        '''Address of the underlying pw_loop.'''
        return self._native.main_loop_get_loop(self._require())

    def run(self: Self) -> int:
        '''Block and dispatch events until quit() is called. Returns the `pw_main_loop_run()` result.'''
        return self._native.main_loop_run(self._require())

    def quit(self: Self) -> int:
        '''Ask a running loop to stop. Safe to call from callbacks on the loop thread.'''
        return self._native.main_loop_quit(self._require())

    def close(self: Self) -> None:
        '''Close the loop (call `pw_main_loop_destroy()` and set the handle to None).'''
        if self._handle is not None:
            self._native.main_loop_destroy(self._handle)
            self._handle = None

    def _require(self: Self) -> int:
        '''Return self._handle, raise an error if None.'''
        if self._handle is None:
            raise PipeWireError('MainLoop is closed')
        return self._handle