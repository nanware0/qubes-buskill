# qubesadmin imports
import qubesadmin # pyright: ignore[reportMissingTypeStubs]
from qubesadmin.app import QubesBase, QubesLocal # pyright: ignore[reportMissingTypeStubs]

def kill_qubes(qubes: list[str]) -> None:
    '''
    Kill qubes in the list of qubes' name.  
    Ignore non existent qubes or dom0, 
    if the list contains '@all', 
    kill every qube except dom0.

    :param qubes: List of qubes to kill's name.
    '''

    app: QubesBase = qubesadmin.Qubes()

    if isinstance(app, QubesLocal):
        if '@all' in qubes:
            for vm in app.domains:
                if vm.klass != 'AdminVM': # type: ignore
                    vm.kill()
        else:
            for vm in app.domains:
                if vm.name in qubes and vm.klass != 'AdminVM': # type: ignore
                    vm.kill()