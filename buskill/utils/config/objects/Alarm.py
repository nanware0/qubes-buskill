# buskill imports
from buskill.utils.config.objects.types import TypedConfig, EncodedTypedConfig

class AlarmConfig(TypedConfig, EncodedTypedConfig):
    freq_low: int
    freq_high: int
    sweep_freq: float
    amplitude: float