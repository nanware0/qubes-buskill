# The package policy is that every step must be commented 
# and that documenting the code is an obligation, 
# don't be afraid by the comments,
# they're here to specify the expected behavior

# qubesadmin imports
import qubesadmin # pyright: ignore[reportMissingTypeStubs]
from qubesadmin.app import QubesBase, QubesLocal # pyright: ignore[reportMissingTypeStubs]
from qubesadmin.vm import QubesVM # pyright: ignore[reportMissingTypeStubs]

def get_qube_for_permanent_edit(qube: str) -> str:
    '''
    Some USB Qubes can be Named DisposableVM, 
    in that case, 
    we should edit the DisposableTemplate instead of the USB Qube.
    
    Returns:
        The name of the Qube to edit for permanent edits.

    :param qube: The name of the USB Qube.
    '''

    app: QubesBase = qubesadmin.Qubes() # Initialize a Qubes application object communicating through qrexec services

    if isinstance(app, QubesLocal):
        vm: QubesVM | None = app.domains.get(qube, default=None)
        if vm is not None: # The VM should exist
            # Verify types of property to access
            # QubesVM.klass, QubesVM.template and QubesVM.name are unknown
            if isinstance(vm.template, QubesVM) and isinstance(vm.klass, str): # pyright: ignore[reportUnknownMemberType]
                if vm.klass == 'DispVM': # If the qube is a DisposableVM, need to edit the qube's template for permanent edits
                    return vm.template.name # Return the qube's template's name
                
                # If the Qube is an AppVM (a disposable template is an AppVM), a StandaloneVM, a TemplateVM, or an AdminVM)
                # (this last two cases should not be used)
                else:
                    return qube # Return the Qube itself
            
    return '@unknown' # Return an exception value ('@' is an illegal character in the qube's name so there is no conflict)