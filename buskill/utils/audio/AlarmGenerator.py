# numpy imports
import numpy
from numpy import float64, float32, int_
from numpy.typing import NDArray

# typing imports
from typing import Self, Protocol, Literal

# sounddevice imports
import sounddevice as sd # pyright: ignore[reportMissingTypeStubs]

# subprocess imports
import subprocess

# re imports
import re

# buskill imports
from buskill.utils import COMMANDS

class TimeInfoProtocol(Protocol):
    '''
    Protocol for time_info's type.
    '''
    inputBufferAdcTime: float
    currentTime: float
    outputBufferDacTime: float

class AlarmGenerator():
    '''
    The alarm generator class. Includes everything to start an alarm without trouble.  
    NOT FINISHED YET
    '''

    def __init__(
        self: Self,
        chunk_size: int = 2048,
        freq_low: int = 800,
        freq_high: int = 1600,
        sweep_freq: float = 7,
        amplitude: float = 0.93
    ) -> None:
        self.started: bool = False

        self.sample_rate: int = 44100
        self.chunk_size: int = chunk_size
        self.freq_low: int = freq_low
        self.freq_high: int = freq_high
        self.sweep_freq: float = sweep_freq
        self.amplitude: float = amplitude

        self.phase: float = 0
        self.sample_generated: int = 0

        self.default_sink: int = -1

    def _run(
        self: Self, 
        command: list[str], 
        check: bool = False
    ) -> subprocess.CompletedProcess[str]:
        '''
        Run wpctl.
        '''
        return subprocess.run(
            [COMMANDS['WPCTL'], *command],
            check=check, 
            capture_output=True, 
            text=True
        )

    def callback(
        self: Self, 
        outdata: NDArray[float32], 
        frames: int,
        info: TimeInfoProtocol,
        status: sd.CallbackFlags
    ) -> None:
        '''
        Callback generating the sawtooth alarm.
        '''
        if status:
            print(f'Error status : {status}')

        sample_indices: NDArray[int_] = numpy.arange(frames)

        chunk_time: NDArray[float64] = sample_indices / self.sample_rate

        t_absolute: float = self.sample_generated / self.sample_rate
        t_full: NDArray[float64] = t_absolute + chunk_time
        freq_modulated: NDArray[float64] = (
            self.freq_low +
            (self.freq_high - self.freq_low) *
            numpy.abs(numpy.sin(2 * numpy.pi * self.sweep_freq * t_full))
        )

        phase_increment: NDArray[float64] = 2 * numpy.pi * freq_modulated / self.sample_rate
        phase_cumsum: NDArray[float64] = numpy.cumsum(phase_increment)
        phase_chunk: NDArray[float64] = self.phase + phase_cumsum

        sawtooth: NDArray[float64] = 2 * ((phase_chunk / (2 * numpy.pi)) % 1.0) - 1
        signal: NDArray[float64] = sawtooth * self.amplitude

        self.phase = phase_chunk[-1]
        self.sample_generated += frames

        outdata[:, 0] = signal.astype(float32)

    def list_sinks(self: Self) -> list[tuple[int, str, bool]]:
        '''
        List sinks using wpctl.  
        Works with older versions of wpctl,
        including the Qubes R4.3 dom0's wpctl version,
        which doesn't support the list command but only the status command.
        '''
        status: str = self._run(['status','-n']).stdout
        sinks_str: str = status.split('├─ Sinks:')[1].split('├─ Sources:')[0]
        sink_lines: list[str] = sinks_str.split('\n')
        sink_lines.pop()
        sink_lines.pop()
        sink_lines.pop(0)
        sinks: list[list[str]] = [re.sub(r' +', ' ', sink_line.strip()).split(' ') for sink_line in sink_lines]
        result: list[tuple[int, str, bool]] = []
        for sink in sinks:
            default: bool = False
            if sink[1] == '*':
                default = True
                sink.pop(1)
                self.default_sink = int(sink[1].removesuffix('.'))
            result.append((int(sink[1].removesuffix('.')), sink[2], default))
        return result

    def set_volume(self: Self, sink: int, volume: float) -> None:
        '''
        Set the volume of a sink.
        '''
        self._run(['set-volume', str(sink), str(volume)])

    def set_mute(self: Self, sink: int, mute: Literal[0, 1, 'toggle']) -> None:
        '''
        Set the mute value of a sink.
        '''
        self._run(['set-mute', str(sink), str(mute)])

    def set_default(self: Self, sink: int):
        '''
        Set a sink as default.
        '''
        self._run(['set-default', str(sink)])
        self.default_sink = sink

    def setup_sinks(self: Self) -> None:
        '''
        Setup the sinks to run the alarm without problem.
        '''
        for sink in self.list_sinks():
            self.set_volume(sink[0], 1.0)
            self.set_mute(sink[0], 0)
            if re.match(r'alsa_output.*.analog-stereo', sink[1]):
                self.set_default(sink[0])
                return

    def get_sample_rate(self: Self) -> int:
        '''
        Return the sample rate of the default sink.
        '''
        properties: list[str] = self._run(['inspect', str(self.default_sink)]).stdout.split('\n')
        for property_line in properties:
            property_line = property_line.strip()
            if property_line.startswith('audio.rate'):
                property: list[str] = property_line.split(' ')
                return int(property[2].replace('"', ''))

        return -1

    def start(self: Self, restart: bool = False) -> bool:
        '''
        Start the alarm.
        '''
        if self.started:
            if restart: self.stop()
            else: return False
        self.setup_sinks()
        sample_rate = self.get_sample_rate()
        self.sample_rate = sample_rate if sample_rate != -1 else 44100
        try:
            self.stream: sd.OutputStream = sd.OutputStream(
                self.sample_rate,
                blocksize=self.chunk_size,
                callback=self.callback
            )
        except Exception as e: 
            print(e)
            return False # We don't want any exception killing the program
        self.stream.start()
        self.started = True
        return True

    def stop(self: Self) -> None:
        '''
        Stop the alarm.
        '''
        self.stream.close()