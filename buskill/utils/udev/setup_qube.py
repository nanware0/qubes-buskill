# buskill imports
from buskill.utils.qubes import run_in_qube
from buskill.utils.udev import generate

# subprocess imports
from subprocess import run

def setup_qube(qube: str, usb_models: set[str]) -> bool:
    if qube != 'dom0':
        worked: bool = True
        worked &= run_in_qube(qube, f'cat << EOF | sudo tee /rw/config/buskill.rules\n{generate(qube, usb_models)}\nEOF')
        worked &= run_in_qube(qube, 'sudo ln -s /rw/config/buskill.rules /etc/udev/rules.d/')
        worked &= run_in_qube(qube, 'sudo udevadm control --reload')
        return worked
    else:
        try:
            run(f'cat << EOF | sudo tee /rw/config/buskill.rules\n{generate(qube, usb_models)}\nEOF', check=True)
            run('sudo ln -s /rw/config/buskill.rules /etc/udev/rules.d/')
            run('sudo udevadm control --reload')
            return True
        except: return False