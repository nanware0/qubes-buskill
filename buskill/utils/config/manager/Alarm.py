# typing imports
from typing import Self

# buskill imports
from buskill.utils.config.objects import AlarmConfig
from buskill.utils.config.manager import Manager, ApplyFunc

class AlarmManager(Manager):
    def __init__(self: Self, apply: ApplyFunc) -> None:
        self._config: AlarmConfig
        self._apply: ApplyFunc = apply

    def apply(self: Self, param_path: list[str]) -> None:
        param_path.insert(0, 'alarm')
        self._apply(param_path)

    def load_config(self: Self, config: AlarmConfig) -> None:
        self._config = config
        self.apply([])

    def change_freq_low(self: Self, freq_low: int) -> None:
        self._config['freq_low'] = freq_low
        self.apply(['freq_low'])

    def change_freq_high(self: Self, freq_high: int) -> None:
        self._config['freq_high'] = freq_high
        self.apply(['freq_high'])

    def change_sweep_freq(self: Self, sweep_freq: float) -> None:
        self._config['sweep_freq'] = sweep_freq
        self.apply(['sweep_freq'])

    def change_amplitude(self: Self, amplitude: float) -> None:
        self._config['amplitude'] = amplitude
        self.apply(['amplitude'])

    @property
    def freq_low(self: Self) -> int:
        return self._config['freq_low']

    @property
    def freq_high(self: Self) -> int:
        return self._config['freq_high']

    @property
    def sweep_freq(self: Self) -> float:
        return self._config['sweep_freq']

    @property
    def amplitude(self: Self) -> float:
        return self._config['amplitude']

    @property
    def get(self: Self) -> AlarmConfig:
        return self._config

    @property
    def encoded(self: Self) -> AlarmConfig:
        return self._config

    def decode(self: Self, encoded_config: AlarmConfig) -> AlarmConfig:
        return encoded_config