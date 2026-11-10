# enum imports
from enum import Enum

# typing imports
from typing import Literal

class Verbose(Enum):
    '''
    The levels of verbose.  
    - `NONE` = nothing is logged.
    - `HIGHEST` = everything is logged.
    '''
    NONE = 0
    NORMAL = 1
    HIGHER = 2
    HIGHEST = 3

class LogType(Enum):
    '''
    The type of log.  
    - `LOG` - a normal log.
    - `OK` - a confirmation that something worked.
    - `WARNING` - a basic warning, but no error yet.
    - `ERROR` - an error occured and we need to log it.
    '''
    LOG = 0
    OK = 1
    WARNING = 2
    ERROR = 3

class Color():
    '''
    Some ASCII colors used by the logger.
    '''
    RED: Literal['\033[91m'] = '\033[91m'
    GREEN: Literal['\033[92m'] = '\033[92m'
    YELLOW: Literal['\033[93m'] = '\033[93m'
    END: Literal['\033[0m'] = '\033[0m'