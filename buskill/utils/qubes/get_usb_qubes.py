# The package policy is that every step must be commented 
# and that documenting the code is an obligation, 
# don't be afraid by the comments,
# they're here to specify the expected behavior

# qubesadmin imports
import qubesadmin # pyright: ignore[reportMissingTypeStubs]
from qubesadmin.devices import DeviceCollection # pyright: ignore[reportMissingTypeStubs]
from qubesadmin.device_protocol import DeviceCategory # pyright: ignore[reportMissingTypeStubs]
from qubesadmin.app import QubesBase, QubesLocal # pyright: ignore[reportMissingTypeStubs]

# buskill.utils.qubes
from buskill.utils.qubes.USBQubesType import USBQubesType

def get_usb_qubes(qubes_type: USBQubesType) -> set[str]:
    '''
    Qubes OS utility function.
    Returns:
        A set containing the names of the USB Qubes (of the specific type qubes_type)

    :param qubes_type: The type of USB Qubes to list.
    '''
    app: QubesBase = qubesadmin.Qubes() # Initialize a Qubes application object communicating through qrexec services

    if isinstance(app, QubesLocal):
        usb_qubes: set[str] = set() # Initialize the set containing the USB Qubes

        # We iterate on the domains.
        for vm in app.domains:

            # We deal with dom0 somewhere else
            if vm.klass != "AdminVM": # pyright: ignore[reportUnknownMemberType]

                device_collection: DeviceCollection = DeviceCollection(vm=vm, class_="pci") # Initialize the DeviceCollection object of the qube

                # CASE 1 : We consider qubes with at least one PCI_USB device assigned as USB Qubes
                if (qubes_type == USBQubesType.ASSIGNED or qubes_type == USBQubesType.BOTH) and vm.name not in usb_qubes:
                    for assignment in device_collection.get_assigned_devices(): # Enumerates the assigned devices
                        for interface in assignment.device.interfaces: # Enumerates the interface of the assigned device
                            if interface.category == DeviceCategory.PCI_USB: # Verify if it's a PCI_USB
                                usb_qubes.add(vm.name) # Add the qube name to the set
                                break # No need to enumerate the remaining interfaces

                        if vm.name in usb_qubes: break # No need to enumerate the remaining assigned devices

                # CASE 2 : We consider qubes with at least one PCI_USB device attached as USB Qubes
                if (qubes_type == USBQubesType.CURRENTLY_USED or qubes_type == USBQubesType.BOTH) and vm.name not in usb_qubes:
                    for assignment in device_collection.get_attached_devices(): # Enumerates the attached devices
                        for interface in assignment.device.interfaces: # Enumerates the interface of the attached device
                            if interface.category == DeviceCategory.PCI_USB: # Verify if it's a PCI_USB
                                usb_qubes.add(vm.name) # Add the qube name to the set
                                break # No need to enumerate the remaining interfaces

                        if vm.name in usb_qubes: break # No need to enumerate the remaining attached devices

        return usb_qubes
    else: return set()