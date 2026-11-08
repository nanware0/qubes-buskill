# subprocess imports
import subprocess

# setuptools imports
from setuptools.build_meta import (
    build_wheel as _build_wheel,
    build_sdist as _build_sdist
)
from setuptools._path import StrPath # type: ignore
from setuptools.build_meta import _ConfigSettings # type: ignore

def _generate_stubs():
    result = subprocess.run(
        ['stubgen', '-p', 'buskill', '-o', '.'],
        capture_output=True,
        text=True,
    )
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    print("Return code:", result.returncode)

def build_wheel(wheel_directory: StrPath, config_settings: _ConfigSettings = None, metadata_directory: StrPath | None = None):
    _generate_stubs()
    return _build_wheel(wheel_directory, config_settings, metadata_directory)

def build_sdist(sdist_directory: StrPath, config_settings: _ConfigSettings = None):
    _generate_stubs()
    return _build_sdist(sdist_directory, config_settings)