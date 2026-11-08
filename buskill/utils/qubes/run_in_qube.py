# qubesadmin imports
import qubesadmin # pyright: ignore[reportMissingTypeStubs]
from qubesadmin.app import QubesBase, QubesLocal # pyright: ignore[reportMissingTypeStubs]
from qubesadmin.vm import QubesVM # pyright: ignore[reportMissingTypeStubs]

def run_in_qube(qube: str, command: str) -> bool:
    app: QubesBase = qubesadmin.Qubes() # Initialize a Qubes application object communicating through qrexec services
    
    if isinstance(app, QubesLocal):
        vm: QubesVM | None = app.domains.get(qube, None)
        if vm is not None:
            try:
                vm.run(command) # pyright: ignore[reportUnknownMemberType]
            except: return False
    return False