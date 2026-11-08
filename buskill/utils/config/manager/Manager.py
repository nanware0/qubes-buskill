# typing imports
from typing import Self, Any

# buskill imports
from buskill.utils.config.objects.types import TypedConfig, EncodedTypedConfig
from buskill.utils.config.manager import ApplyFunc

# abc imports
from abc import ABC, abstractmethod

# dataclasses import
from dataclasses import dataclass

@dataclass
class Manager(ABC):
    _config: Any
    _apply: ApplyFunc

    @abstractmethod
    def __init__(self: Self) -> None: ...

    @abstractmethod
    def apply(self: Self, param_path: list[str]) -> None: ...

    @abstractmethod
    def load_config(self: Self, config: Any) -> None: ...

    @property
    @abstractmethod
    def get(self: Self) -> TypedConfig: ...

    @property
    @abstractmethod
    def encoded(self: Self) -> EncodedTypedConfig: ...

    @abstractmethod
    def decode(self: Self, encoded_config: Any) -> TypedConfig: ...