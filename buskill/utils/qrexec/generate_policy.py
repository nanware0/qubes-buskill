# datetime imports
from datetime import datetime

def generate_policy(armed_qubes: set[str]) -> str:
    header: str = f'''################################################################################
# File:           dom0:/etc/qubes/policy.d/30-buskill.policy
# Purpose:        Add buskill rules. For more info, see: https://github.com/nanware0/qubes-buskill-doc
# Authors:        Michael Altfield <michael@buskill.in>, Nanware <nanware@pm.me>
# Auto-generated: {datetime.now()}
# License:        GNU GPLv3
################################################################################'''
    result: list[str] = [header]
    for qube in armed_qubes:
        result.append(f'qubes.BusKill +activate {qube} dom0 allow')
    return '\n'.join(result)