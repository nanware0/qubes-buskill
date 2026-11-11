# typing imports
from typing import Self, Callable, Any

# buskill imports
from buskill.utils.audio import AlarmGenerator
# config
from buskill.utils.config.manager import CONFIG_MANAGER, ConfigManager
from buskill.utils.config.objects import Action
# actions
from buskill.utils.actions import self_destruct, lock_screen, shutdown, reboot
# delay_execution
from buskill.utils import delay_execution
# qubes
from buskill.utils.qubes import kill_qubes
# udev
from buskill.utils.udev import setup_qube
# qrexec
from buskill.utils.qrexec import write_policy

# asyncio imports
import asyncio
from asyncio import AbstractEventLoop, Future

# threading imports
from threading import Thread

class Buskill():
    def __init__(self: Self) -> None:
        CONFIG_MANAGER.set_apply_func(self.apply)
        self.loop: AbstractEventLoop = asyncio.new_event_loop()
        thread: Thread = Thread(target=self.loop.run_forever, daemon=True)
        thread.start()
        self.alarm: AlarmGenerator = AlarmGenerator(
            freq_low=CONFIG_MANAGER.alarm.freq_low,
            freq_high=CONFIG_MANAGER.alarm.freq_high,
            sweep_freq=CONFIG_MANAGER.alarm.sweep_freq,
            amplitude=CONFIG_MANAGER.alarm.amplitude
        )

    @property
    def config(self: Self) -> ConfigManager:
        return CONFIG_MANAGER

    def apply_armed_qubes(self: Self) -> None:
        write_policy(CONFIG_MANAGER.general.armed_qubes)

    async def apply_usb(self: Self) -> None:
        writes: list[Future[bool]] = []
        for qube in CONFIG_MANAGER.general.usb.qubes:
            writes.append(self.loop.run_in_executor(None, setup_qube, qube, CONFIG_MANAGER.general.usb.models))
        if CONFIG_MANAGER.general.use_dom0:
            writes.append(self.loop.run_in_executor(None, setup_qube, 'dom0', CONFIG_MANAGER.general.usb.models))

        await asyncio.gather(*writes)

    def apply(self: Self, param_path: list[str]) -> None:
        path_length: int = len(param_path)
        if path_length > 0 and param_path[0] == 'config':
            if path_length < 3:
                self.loop.run_in_executor(None, self.apply_armed_qubes)
                self.loop.run_in_executor(None, self.apply_usb)
            elif param_path[1] == 'general':
                if param_path[2] == 'armed_qubes':
                    self.loop.run_in_executor(None, self.apply_armed_qubes)
                elif (param_path[2] == 'usb' and not 'qubes_type' in param_path) or param_path[2] == 'use_dom0': 
                    self.loop.run_in_executor(None, self.apply_usb)
        if CONFIG_MANAGER.system.auto_save:
            CONFIG_MANAGER.save()

    def _setup_fallback(self: Self) -> None:
        if CONFIG_MANAGER.action.fallback.delay == 0: 
            return
        fallback: Callable[..., Any]
        args: list[bool] = []

        if CONFIG_MANAGER.action.fallback.action == Action.REBOOT: 
            fallback = reboot
            args.append(CONFIG_MANAGER.action.hard)
        elif CONFIG_MANAGER.action.fallback.action == Action.SHUTDOWN: 
            fallback = shutdown
            args.append(CONFIG_MANAGER.action.hard)
        else: fallback = self_destruct

        self.loop.create_task(
            delay_execution(
                CONFIG_MANAGER.action.fallback.delay,
                {
                    'func': fallback,
                    'args': args,
                    'kwargs': {}
                }
            )
        )

    def activate(self: Self) -> None:
        if CONFIG_MANAGER.action.action == Action.LOCK:
            self.loop.run_in_executor(None, lock_screen)
            self._setup_fallback()
        elif CONFIG_MANAGER.action.action == Action.ALARM:
            self.loop.run_in_executor(None, lock_screen)
            self.loop.run_in_executor(None, kill_qubes, ['@all'])
            self.loop.run_in_executor(None, self.alarm.start)
            self._setup_fallback()
        elif CONFIG_MANAGER.action.action == Action.REBOOT:
            reboot(CONFIG_MANAGER.action.hard)
        elif CONFIG_MANAGER.action.action == Action.SHUTDOWN:
            shutdown(CONFIG_MANAGER.action.hard)
        else:
            if asyncio.run(self_destruct()) == False:
                shutdown(CONFIG_MANAGER.action.hard)