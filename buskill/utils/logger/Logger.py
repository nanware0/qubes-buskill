# typing imports
from typing import Self

# datetime imports
from datetime import datetime

# pathlib imports
from pathlib import Path

# buskill imports
from buskill.utils.logger import Verbose, LogType, Color

# shutil imports
import shutil

class Logger():
    '''
    A basic logger that contains the type of the logs and their timestamp, and is able to save them.  
    It is not finished yet.
    '''
    log_dir: Path = Path('/var/lib/qubes-buskill')
    log_path: Path = log_dir / 'buskill.log'
    
    def __init__(self: Self, verbose: Verbose, log_history_len: int = 2000) -> None:
        '''
        Initialize the logger and configure the level of verbose of the logs, and the number of logs saved.
        '''
        self.logs: list[str] = []
        self.verbose: Verbose = verbose
        if log_history_len <= 0:
            self.log_history_len = 2000
        else: self.log_history_len: int = log_history_len

    def log(self: Self, log: str, log_verbose: Verbose, type: LogType = LogType.LOG) -> None:
        '''Print a log and save it'''
        if self.verbose.value >= log_verbose.value:
            date: datetime = datetime.now()
            log_string: str
            if type == LogType.LOG:
                log_string = f'{date} - LOG: {log}'
            elif type == LogType.OK:
                log_string = f'{Color.GREEN}{date} - OK: {log}{Color.END}'
            elif type == LogType.WARNING:
                log_string = f'{Color.YELLOW}{date} - WARNING: {log}{Color.END}'
            else:
                log_string = f'{Color.RED}{date} - ERROR: {log}{Color.END}'

            print(log_string)
            if len(self.logs) >= self.log_history_len:
                self.logs = self.logs[-self.log_history_len:]
            self.logs.append(log_string)

    def save(self: Self) -> None:
        if not self.log_dir.exists():
            self.log_dir.mkdir(parents=True)
        elif not self.log_dir.is_dir():
            self.log_dir.unlink()
            self.log_dir.mkdir(parents=True)

        if self.log_path.is_dir():
            shutil.rmtree(self.log_path)

        self.log_path.write_text('\n'.join(self.logs))