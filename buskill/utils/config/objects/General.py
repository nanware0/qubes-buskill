# typing imports
from typing import Literal

# buskill imports
from buskill.utils.qubes import USBQubesType
from buskill.utils.config.objects.types import TypedConfig, EncodedTypedConfig

class USBConfig(TypedConfig):
    models: set[str]
    qubes: set[str]
    qubes_type: USBQubesType

class GeneralConfig(TypedConfig):
    self_destruct_authorized: bool
    armed: bool
    use_dom0: bool
    armed_qubes: set[str]
    usb: USBConfig

type EncodedUSBQubesType = Literal[0, 1, 2]

class EncodedUSBConfig(EncodedTypedConfig):
    models: list[str]
    qubes: list[str]
    qubes_type: EncodedUSBQubesType

class EncodedGeneralConfig(EncodedTypedConfig):
    self_destruct_authorized: bool
    armed: bool
    use_dom0: bool
    armed_qubes: list[str]
    usb: EncodedUSBConfig