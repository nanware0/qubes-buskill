# datetime imports
from datetime import datetime

def generate(qube: str, usb_models: set[str]) -> str:
    header: str = f'''################################################################################
# File:           {qube}:/etc/udev/rules.d/buskill.rules -> /rw/config/buskill.rules
# Purpose:        Add buskill rules. For more info, see: https://github.com/nanware0/qubes-buskill-doc
# Authors:        Michael Altfield <michael@buskill.in>, Nanware <nanware@pm.me>
# Auto-generated: {datetime.now()}
# License:        GNU GPLv3
################################################################################'''
    command: str = '/usr/bin/qrexec-client-vm dom0 buskill.activate' if not qube == 'dom0' else '/usr/bin/buskill-cli activate'
    udev_lines: list[str] = [header]
    if len(usb_models) > 0:
        for model in usb_models:
            udev_lines.append(f'ACTION="remove", SUBSYSTEM="usb", ENV{{ID_MODEL}}=="{model}", RUN+="{command}"')
    else:
        return header + f'\nACTION="remove", SUBSYSTEM="usb", RUN+="{command}"'
    return '\n'.join(udev_lines)