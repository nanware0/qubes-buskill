class PipeWireError(RuntimeError):
    """A libpipewire call failed or was used in an invalid state."""


class PipeWireLibraryNotFoundError(PipeWireError):
    """libpipewire-0.3 could not be loaded."""