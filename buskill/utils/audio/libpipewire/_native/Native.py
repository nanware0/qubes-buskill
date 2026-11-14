# ctypes imports
import ctypes
from ctypes import (
    CDLL, POINTER,
    c_char_p, c_int, c_void_p
)

# abc imports
from collections.abc import Sequence

# buskill imports
from buskill.utils.audio.libpipewire._native import require_handle

# typing imports
from typing import Self

class Native():
    '''The only place where ctypes signatures are declared.'''

    def __init__(self: Self, lib: CDLL) -> None:
        '''Initialize a Native object with libpipewire using ctypes.'''
        self._lib: CDLL = lib
        # Keeps argv memory alive for as long as PipeWire may reference it.
        self._keepalive: list[object] = []

        lib.pw_init.argtypes = [POINTER(c_int), POINTER(POINTER(c_char_p))]
        lib.pw_init.restype = None

        lib.pw_deinit.argtypes = []
        lib.pw_deinit.restype = None

        lib.pw_main_loop_new.argtypes = [c_void_p]
        lib.pw_main_loop_new.restype = c_void_p

        lib.pw_main_loop_get_loop.argtypes = [c_void_p]
        lib.pw_main_loop_get_loop.restype = c_void_p

        lib.pw_main_loop_run.argtypes = [c_void_p]
        lib.pw_main_loop_run.restype = c_int

        lib.pw_main_loop_quit.argtypes = [c_void_p]
        lib.pw_main_loop_quit.restype = c_int

        lib.pw_main_loop_destroy.argtypes = [c_void_p]
        lib.pw_main_loop_destroy.restype = None

    def init(self: Self, argv: Sequence[str]) -> None:
        '''
        Initialize the PipeWire system, parse and modify any parameters given by argv and set up debugging.

        This function can be called multiple times. 
        '''
        count: int = len(argv)
        encoded: list[bytes | None] = [arg.encode("utf-8") for arg in argv]
        encoded.append(None)  # argv must be NULL-terminated
        argv_array = (c_char_p * (count + 1))(*encoded)
        argv_ptr = ctypes.cast(argv_array, POINTER(c_char_p))
        argc = c_int(count)

        self._keepalive.extend([argv_array, argv_ptr, argc])
        self._lib.pw_init(ctypes.byref(argc), ctypes.byref(argv_ptr))

    def deinit(self: Self) -> None:
        '''
        Deinitialize the PipeWire system and free up all resources allocated by pw_init().

        Before 0.3.49 this function can only be called once after which the pipewire library can not be used again.
        This is usually called by test programs to check for memory leaks.

        Since 0.3.49 this function must be paired with an equal amount of pw_init() calls to deinitialize the PipeWire library.
        The PipeWire library can be used again after being deinitialized with a new pw_init() call.
        '''
        self._lib.pw_deinit()
        self._keepalive.clear()

    def main_loop_new(self: Self) -> int:
        '''
        Create a new main loop.

        Returns:
            a newly allocated Main Loop 
        '''
        handle: int | None = self._lib.pw_main_loop_new(None)
        return require_handle(handle, 'pw_main_loop_new')

    def main_loop_get_loop(self: Self, loop: int) -> int:
        '''Get the loop implementation.'''
        handle: int | None = self._lib.pw_main_loop_get_loop(loop)
        return require_handle(handle, 'pw_main_loop_get_loop')

    def main_loop_run(self: Self, loop: int) -> int:
        '''
        Run a main loop.

        Returns:
            0 on success, otherwise a negative number.

        :param loop: the main loop to start

        Start running loop. This function blocks until `pw_main_loop_quit()` has been called 
        '''
        result: int = self._lib.pw_main_loop_run(loop)
        return result

    def main_loop_quit(self: Self, loop: int) -> int:
        '''
        Quit a main loop.

        :param loop:a Main Loop to stop

        The call to `pw_main_loop_run()` will return 
        '''
        result: int = self._lib.pw_main_loop_quit(loop)
        return result

    def main_loop_destroy(self: Self, loop: int) -> None:
        '''
        Destroy a loop.

        :param loop: the main loop to destroy 
        '''
        self._lib.pw_main_loop_destroy(loop)