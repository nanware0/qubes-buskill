# enum imports
from enum import Enum

# typing imports
from typing import Literal

class Verbose(Enum):
    NONE = 0
    NORMAL = 1
    HIGHER = 2
    HIGHEST = 3

class LogType(Enum):
    LOG = 0
    OK = 1
    WARNING = 2
    ERROR = 3

class Color():
    RED: Literal['\033[91m'] = '\033[91m'
    GREEN: Literal['\033[92m'] = '\033[92m'
    YELLOW: Literal['\033[93m'] = '\033[93m'
    END: Literal['\033[0m'] = '\033[0m'