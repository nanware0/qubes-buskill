# enum imports
from enum import Enum

# typing imports
from typing import Literal

# buskill imports
from buskill.utils.config.objects.types import TypedConfig, EncodedTypedConfig

class Action(Enum):
    LOCK = 0
    ALARM = 1
    REBOOT = 2
    SHUTDOWN = 3
    SELF_DESTRUCT = 4

type FallbackAction = Literal[Action.REBOOT, Action.SHUTDOWN, Action.SELF_DESTRUCT]

class FallbackConfig(TypedConfig):
    action: FallbackAction
    delay: int

class ActionConfig(TypedConfig):
    hard: bool
    action: Action
    fallback: FallbackConfig

type EncodedAction = Literal[0, 1, 2, 3, 4]
type EncodedFallbackAction = Literal[2, 3, 4]

class EncodedFallbackConfig(EncodedTypedConfig):
    action: EncodedFallbackAction
    delay: int

class EncodedActionConfig(EncodedTypedConfig):
    hard: bool
    action: EncodedAction
    fallback: EncodedFallbackConfig