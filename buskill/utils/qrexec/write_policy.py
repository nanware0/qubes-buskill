# pathlib imports
from pathlib import Path

# shutil imports
import shutil

# os imports
import os

# buskill imports
from buskill.utils.qrexec import generate_policy

def write_policy(armed_qubes: set[str]) -> None:
    policy_path: Path = Path('/etc/qubes/policy.d/30-buskill.policy')
    if policy_path.is_dir():
        shutil.rmtree(policy_path)

    policy_path.write_text(generate_policy(armed_qubes))
    with open(policy_path, 'rb') as f:
        os.fsync(f.fileno())