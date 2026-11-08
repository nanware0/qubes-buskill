# typing imports
from typing import Self

# buskill imports
from buskill.utils.config.objects import SystemConfig
from buskill.utils.config.manager import Manager, ApplyFunc
from buskill.utils.logger import Verbose

class SystemManager(Manager):
    def __init__(self: Self, apply: ApplyFunc) -> None:
        self._config: SystemConfig
        self._apply: ApplyFunc = apply

    def apply(self: Self, param_path: list[str]) -> None:
        param_path.insert(0, 'system')
        self._apply(param_path)

    def load_config(self: Self, config: SystemConfig) -> None:
        self._config = config

    def set_auto_save(self: Self, auto_save: bool) -> None:
        self._config['auto_save'] = auto_save
        self.apply(['auto_save'])

    def set_refresh_when_starting(self: Self, refresh_when_starting: bool) -> None:
        self._config['refresh_when_starting'] = refresh_when_starting
        self.apply(['refresh_when_starting'])

    def set_verbose(self: Self, verbose: Verbose) -> None:
        self._config['verbose'] = verbose
        self.apply(['verbose'])

    @property
    def auto_save(self: Self) -> bool:
        return self._config['auto_save']

    @property
    def refresh_when_starting(self: Self) -> bool:
        return self._config['refresh_when_starting']

    @property
    def log(self: Self) -> Verbose:
        return self._config['verbose']

    @property
    def get(self: Self) -> SystemConfig:
        return self._config

    @property
    def encoded(self: Self) -> SystemConfig:
        return self._config

    def decode(self: Self, encoded_config: SystemConfig) -> SystemConfig:
        return encoded_config