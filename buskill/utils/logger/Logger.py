# typing imports
from typing import Self

# datetime imports
from datetime import datetime

# pathlib imports
from pathlib import Path

# buskill imports
from buskill.utils.logger import Verbose, LogType, Color

class Logger():
    '''
    A basic logger that contains the type of the logs and their timestamp, and is able to save them.  
    It is not finished yet.
    '''
    log_dir: Path = Path('/var/lib/qubes-buskill')
    
    def __init__(self: Self, verbose: Verbose, log_history_len: int = 2000) -> None:
        '''
        Initialize the logger and configure the level of verbose of the logs, and the number of logs saved.
        '''
        self.logs: list[tuple[datetime, Verbose, LogType, str]] = []
        self.verbose: Verbose = verbose
        if log_history_len <= 0:
            self.log_history_len = 2000
        else: self.log_history_len: int = log_history_len

    def log(self: Self, log: str, log_verbose: Verbose, type: LogType = LogType.LOG) -> None:
        '''Print a log and save it'''
        if self.verbose.value >= log_verbose.value:
            date: datetime = datetime.now()
            if type == LogType.LOG:
                print(f'{date} - LOG: {log}')
            elif type == LogType.OK:
                print(f'{Color.GREEN}{date} - OK: {log}{Color.END}')
            elif type == LogType.WARNING:
                print(f'{Color.YELLOW}{date} - WARNING: {log}{Color.END}')
            else:
                print(f'{Color.RED}{date} - ERROR: {log}{Color.END}')
            
            if len(self.logs) >= self.log_history_len:
                self.logs = self.logs[-self.log_history_len:]
            self.logs.append((date, log_verbose, type, log))

    def save(self: Self) -> None:
        '''Not implemented yet'''
        ...