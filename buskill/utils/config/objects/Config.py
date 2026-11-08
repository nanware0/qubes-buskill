# buskill imports
from buskill.utils.config.objects import (
    SystemConfig, 
    GeneralConfig, 
    ActionConfig, 
    AlarmConfig, 
    RecoveryConfig, 
    EncodedGeneralConfig, 
    EncodedActionConfig,
    EncodedRecoveryConfig
)
from buskill.utils.config.objects.types import (
    TypedConfig,
    EncodedTypedConfig
)

class Config(TypedConfig):
    system_config: SystemConfig
    general_config: GeneralConfig
    action_config: ActionConfig
    alarm_config: AlarmConfig
    recovery_config: RecoveryConfig
    
class EncodedConfig(EncodedTypedConfig):
    system_config: SystemConfig
    general_config: EncodedGeneralConfig
    action_config: EncodedActionConfig
    alarm_config: AlarmConfig
    recovery_config: EncodedRecoveryConfig