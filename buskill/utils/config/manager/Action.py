# typing imports
from typing import Self, cast

# buskill imports
from buskill.utils.config.objects import (
    ActionConfig, 
    Action, 
    FallbackConfig, 
    FallbackAction, 
    EncodedFallbackConfig, 
    EncodedActionConfig
)
from buskill.utils.config.manager import Manager, ApplyFunc

class FallbackManager(Manager):
    def __init__(self: Self, apply: ApplyFunc) -> None:
        self._config: FallbackConfig
        self._apply: ApplyFunc = apply

    def apply(self: Self, param_path: list[str]) -> None:
        param_path.insert(0, 'fallback')
        self._apply(param_path)

    def load_config(self: Self, config: FallbackConfig) -> None:
        self._config = config
        self.apply([])

    def change_action(self: Self, action: FallbackAction) -> None:
        self._config['action'] = action
        self.apply(['action'])

    def change_delay(self: Self, delay: int) -> None:
        self._config['delay'] = delay
        self.apply(['delay'])

    @property
    def action(self: Self) -> FallbackAction:
        return self._config['action']

    @property
    def delay(self: Self) -> int:
        return self._config['delay']

    @property
    def get(self: Self) -> FallbackConfig:
        return self._config

    @property
    def encoded(self: Self) -> EncodedFallbackConfig: 
        return {
            'action': self.action.value,
            'delay': self.delay
        }

    def decode(self: Self, encoded_config: EncodedFallbackConfig) -> FallbackConfig:
        return {
            'action': cast(FallbackAction, Action(encoded_config['action'])),
            'delay': encoded_config['delay']
        }

class ActionManager(Manager):
    def __init__(self: Self, apply: ApplyFunc) -> None:
        self._config: ActionConfig
        self._apply: ApplyFunc = apply
        self.fallback: FallbackManager = FallbackManager(self.apply)

    def apply(self: Self, param_path: list[str]) -> None:
        param_path.insert(0, 'action')
        self._apply(param_path)

    def load_config(self: Self, config: ActionConfig) -> None:
        self._config = config
        self.fallback.load_config(self._config['fallback'])
        self.apply([])

    def set_soft(self: Self) -> None:
        self._config['hard'] = False
        self.apply(['hard'])

    def set_hard(self: Self) -> None:
        self._config['hard'] = True
        self.apply(['hard'])

    def change_action(self: Self, action: Action) -> None:
        self._config['action'] = action
        self.apply(['action'])

    def change_fallback(self: Self, fallback: FallbackConfig) -> None:
        self._config['fallback'] = fallback
        self.fallback.load_config(self._config['fallback'])
        self.apply(['fallback'])

    @property
    def hard(self: Self) -> bool:
        return self._config['hard']

    @property
    def action(self: Self) -> Action:
        return self._config['action']

    @property
    def get(self: Self) -> ActionConfig:
        return self._config

    @property
    def encoded(self: Self) -> EncodedActionConfig:
        return {
            'action': self.action.value,
            'hard': self.hard,
            'fallback': self.fallback.encoded
        }

    def decode(self: Self, encoded_config: EncodedActionConfig) -> ActionConfig:
        return {
            'action': Action(encoded_config['action']),
            'hard': encoded_config['hard'],
            'fallback': self.fallback.decode(encoded_config['fallback'])
        }