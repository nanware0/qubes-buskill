# enum imports
from enum import Enum

class USBQubesType(Enum):
    '''
    Attributes:
        ASSIGNED: Qubes with assigned PCI_USB devices  
        CURRENTLY_USED: Qubes with currently attached (used) PCI_USB devices  
        BOTH: Both types
    '''
    ASSIGNED=0
    CURRENTLY_USED=1
    BOTH=2