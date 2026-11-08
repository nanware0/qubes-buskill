# typing imports
from typing import Self

# buskill imports
from buskill.utils.config.objects import GeneralConfig, USBConfig, EncodedUSBConfig, EncodedGeneralConfig
from buskill.utils.config.manager import Manager, ApplyFunc
from buskill.utils.qubes import USBQubesType, get_usb_qubes

class USBManager(Manager):
    def __init__(self: Self, apply: ApplyFunc) -> None:
        self._config: USBConfig
        self._apply: ApplyFunc = apply

    def apply(self: Self, param_path: list[str]) -> None:
        param_path.insert(0, 'usb')
        self._apply(param_path)

    def load_config(self: Self, config: USBConfig) -> None:
        self._config = config

    def refresh_qubes(self: Self) -> None:
        self._config['qubes'] = get_usb_qubes(self.qubes_type)

    def change_qubes_type(self: Self, qubes_type: USBQubesType) -> None:
        self._config['qubes_type'] = qubes_type

    def add_models(self: Self, models: set[str]) -> None:
        self._config['models'] |= models

    def remove_models(self: Self, models: set[str]) -> None:
        self._config['models'] -= models

    def clear_models(self: Self) -> None:
        self._config['models'].clear()

    def replace_models(self: Self, models: set[str]) -> None:
        self._config['models'] = models

    @property
    def qubes_type(self: Self) -> USBQubesType:
        return self._config['qubes_type']

    @property
    def qubes(self: Self) -> set[str]:
        return self._config['qubes']

    @property
    def models(self: Self) -> set[str]:
        return self._config['models']

    @property
    def get(self: Self) -> USBConfig:
        return self._config

    @property
    def encoded(self: Self) -> EncodedUSBConfig:
        return {
            'models': sorted(list(self.models)),
            'qubes': sorted(list(self.qubes)),
            'qubes_type': self.qubes_type.value
        }

    def decode(self: Self, encoded_config: EncodedUSBConfig) -> USBConfig:
        return {
            'models': set(encoded_config['models']),
            'qubes': set(encoded_config['qubes']),
            'qubes_type': USBQubesType(encoded_config['qubes_type'])
        }

class GeneralManager(Manager):
    def __init__(self: Self, apply: ApplyFunc) -> None:
        self._config: GeneralConfig
        self._apply: ApplyFunc = apply
        self.usb: USBManager = USBManager(self.apply)

    def apply(self: Self, param_path: list[str]) -> None:
        param_path.insert(0, 'general')
        self._apply(param_path)

    def load_config(self: Self, config: GeneralConfig) -> None:
        self._config = config
        self.usb.load_config(self._config['usb'])
        self.apply([])

    def arm(self: Self) -> None:
        self._config['armed'] = True
        self.apply(['armed'])

    def disarm(self: Self) -> None:
        self._config['armed'] = False
        self.apply(['armed'])

    def authorize_self_destruct(self: Self, authorize: bool) -> None:
        self._config['self_destruct_authorized'] = authorize
        self.apply(['self_destruct_author'])

    def arm_qubes(self: Self, qubes: set[str]) -> None:
        self._config['armed_qubes'] |= qubes
        self.apply(['armed_qubes'])

    def disarm_qubes(self: Self, qubes: set[str]) -> None:
        self._config['armed_qubes'] -= qubes
        self.apply(['armed_qubes'])

    def clear_armed_qubes(self: Self) -> None:
        self._config['armed_qubes'].clear()
        self.apply(['armed_qubes'])

    def replace_armed_qubes(self: Self, qubes: set[str]) -> None:
        self._config['armed_qubes'] = qubes
        self.apply(['armed_qubes'])

    def refresh_armed_qubes(self: Self) -> None:
        self._config['armed_qubes'] &= self.usb.qubes
        self.apply(['armed_qubes'])

    def change_usb_config(self: Self, usb_config: USBConfig) -> None:
        self._config['usb'] = usb_config
        self.usb.load_config(self._config['usb'])
        self.apply(['usb'])

    @property
    def armed(self: Self) -> bool:
        return self._config['armed']

    @property
    def self_destruct_authorized(self: Self) -> bool:
        return self._config['self_destruct_authorized']

    @property
    def use_dom0(self: Self) -> bool:
        return self._config['use_dom0']

    @property
    def armed_qubes(self: Self) -> set[str]:
        return self._config['armed_qubes']

    @property
    def get(self: Self) -> GeneralConfig:
        return self._config

    @property
    def encoded(self: Self) -> EncodedGeneralConfig:
        return {
            'armed': self.armed,
            'self_destruct_authorized': self.self_destruct_authorized,
            'use_dom0': self.use_dom0,
            'armed_qubes': sorted(list(self.armed_qubes)),
            'usb': self.usb.encoded
        }

    def decode(self: Self, encoded_config: EncodedGeneralConfig) -> GeneralConfig:
        return {
            'armed': encoded_config['armed'],
            'self_destruct_authorized': encoded_config['self_destruct_authorized'],
            'use_dom0': encoded_config['use_dom0'],
            'armed_qubes': set(encoded_config['armed_qubes']),
            'usb': self.usb.decode(encoded_config['usb'])
        }