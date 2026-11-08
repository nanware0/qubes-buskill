# buskill imports
from buskill.utils.config.objects.types import TypedConfig, EncodedTypedConfig
from buskill.utils.logger import Verbose

class SystemConfig(TypedConfig, EncodedTypedConfig):
    auto_save: bool
    refresh_when_starting: bool
    verbose: Verbose