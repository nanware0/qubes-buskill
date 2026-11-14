# ctypes imports
from ctypes import CDLL

# buskill imports
from buskill.utils.audio.libpipewire._native import PipeWireLibraryNotFoundError, PipeWireError, LIBRARY_NAMES

def load_cdll() -> CDLL:
    '''Load libpipewire-0.3 with ctypes.CDLL.'''
    failures: list[str] = []
    for name in LIBRARY_NAMES:
        try:
            return CDLL(name)
        except OSError as exc:
            failures.append(f"{name}: {exc}")
    raise PipeWireLibraryNotFoundError(
        'could not load libpipewire-0.3 (' + '; '.join(failures) + ')'
    )


def require_handle(value: int | None, function_name: str) -> int:
    '''
    Raise an error if the pointer is NULL, else, return the pointer.

    :param value: The pointer.
    :param function_name: The name of the function that returned the pointer.
    '''
    if value is None or value == 0:
        raise PipeWireError(f'{function_name} returned a NULL pointer')
    return value