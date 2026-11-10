# typing imports
from typing import Self, Any

# pathlib imports
from pathlib import Path

# buskill imports
from buskill.utils.qubes import USBQubesType
from buskill.utils.config.manager import (
    Manager,
    GeneralManager,
    AlarmManager,
    ActionManager,
    RecoveryManager,
    SystemManager,
    ApplyFunc
)
from buskill.utils.config.objects import Config, EncodedConfig, Action
from buskill.utils.logger import Verbose

# json imports
import json

# shutil imports
import shutil

# os imports
import os

class ConfigManager(Manager):
    default_config: Config = {
        'general_config': {
            'armed': False,
            'self_destruct_authorized': False,
            'use_dom0': False,
            'armed_qubes': set(),
            'usb': {
                'qubes': set(),
                'models': {'Micromax_A74'},
                'qubes_type': USBQubesType.ASSIGNED
            }
        },
        'action_config': {
            'hard': False,
            'action': Action.ALARM,
            'fallback': {
                'action': Action.SHUTDOWN,
                'delay': 600
            }
        },
        'alarm_config': {
            'freq_low': 800,
            'freq_high': 1600,
            'sweep_freq': 7,
            'amplitude': 0.93
        },
        'recovery_config': {
            'contact': {
                'emails': set(),
                'phone_numbers': set(),
                'social_medias': {}
            },
            'identity': {
                'first_name': '',
                'family_name': '',
                'date_of_birth': None
            },
            'message': '',
            'enabled': False
        },
        'system_config': {
            'auto_save': True,
            'refresh_when_starting': True,
            'verbose': Verbose.NORMAL
        }
    }

    config_dir: Path = Path('/etc/qubes-buskill/')
    config_path: Path = config_dir / 'config.main'
    backup_config_path: Path = config_dir / 'config.backup'

    def __init__(self: Self) -> None:
        self._config: Config
        self._apply: ApplyFunc

        self.general: GeneralManager = GeneralManager(self.apply)
        self.action: ActionManager = ActionManager(self.apply)
        self.alarm: AlarmManager = AlarmManager(self.apply)
        self.recovery: RecoveryManager = RecoveryManager(self.apply)
        self.system: SystemManager = SystemManager(self.apply)
        self.load()
        if self.system.auto_save:
            self.save()

    def set_apply_func(self: Self, apply: ApplyFunc) -> None:
        self._apply = apply

    def apply(self: Self, param_path: list[str]) -> None:
        param_path.insert(0, 'config')
        if self._apply is not None:
            self._apply(param_path)

    def load_config(self: Self, config: Config) -> None:
        self._config = config
        self.apply([])

    def save(self: Self) -> None:
        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True)
        elif not self.config_dir.is_dir():
            self.config_dir.unlink()
            self.config_dir.mkdir(parents=True)

        data: str = json.dumps(self.encoded)

        if self.config_path.is_dir():
            shutil.rmtree(self.config_path)

        self.config_path.write_text(data)
        self.sync_file(self.config_path)

        if self.backup_config_path.is_dir():
            shutil.rmtree(self.backup_config_path)

        self.backup_config_path.write_text(data)
        self.sync_file(self.backup_config_path)        

    def sync_file(self: Self, file: Path) -> None:
        if file.is_dir(): return
        else:
            try:
                with open(file, 'rb') as f:
                    os.fsync(f.fileno())
            except:
                pass
        
    def load(self: Self) -> None:
        config_file: Path | None = self._get_config_file_and_clean_config()

        if config_file is None:
            self._config = self.default_config
        else:
            self._config = self.decode(json.loads(config_file.read_text()))

        self.general.load_config(self._config['general_config'])
        self.action.load_config(self._config['action_config'])
        self.alarm.load_config(self._config['alarm_config'])
        self.recovery.load_config(self._config['recovery_config'])
        self.system.load_config(self._config['system_config'])

        if config_file is None:
            self.general.usb.refresh_qubes()
            self.general.replace_armed_qubes(self.general.usb.qubes)
        elif self.system.refresh_when_starting:
            self.general.usb.refresh_qubes()
            self.general.refresh_armed_qubes()
        self.apply([])

    def _get_config_file_and_clean_config(self: Self) -> Path | None: 
        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True)
            return None
        elif not self.config_dir.is_dir():
            self.config_dir.unlink()
            self.config_dir.mkdir(parents=True)
            return None
        else:
            for path in self.config_dir.iterdir():
                if path.resolve() not in [self.config_path, self.backup_config_path]:
                    if path.is_dir(): shutil.rmtree(path)
                    else: path.unlink()

            if self.config_path.exists():
                if self.config_path.is_dir():
                    shutil.rmtree(self.config_path)
                elif not self.is_valid(self.config_path.read_text()):
                    self.config_path.unlink()
                else: return self.config_path

            if self.backup_config_path.exists():
                if self.backup_config_path.is_dir():
                    shutil.rmtree(self.backup_config_path)
                elif not self.is_valid(self.backup_config_path.read_text()):
                    self.backup_config_path.unlink()
                else: return self.backup_config_path

            return None

    def is_valid(self: Self, config_json: str) -> bool:
        try:
            data: Any = json.loads(config_json)
            self.decode(data)
            return True
        except:
            return False

    @property
    def get(self: Self) -> Config:
        return self._config

    @property
    def encoded(self: Self) -> EncodedConfig:
        return {
            'general_config': self.general.encoded,
            'action_config': self.action.encoded,
            'alarm_config': self.alarm.encoded,
            'recovery_config': self.recovery.encoded,
            'system_config': self.system.encoded
        }

    def decode(self: Self, encoded_config: EncodedConfig) -> Config:
        return {
            'general_config': self.general.decode(encoded_config['general_config']),
            'action_config': self.action.decode(encoded_config['action_config']),
            'alarm_config': self.alarm.decode(encoded_config['alarm_config']),
            'recovery_config': self.recovery.decode(encoded_config['recovery_config']),
            'system_config': self.system.decode(encoded_config['system_config'])
        }

CONFIG_MANAGER: ConfigManager = ConfigManager()