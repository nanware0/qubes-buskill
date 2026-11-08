# The package policy is that every step must be commented 
# and that documenting the code is an obligation, 
# don't be afraid by the comments,
# they're here to specify the expected behavior

# buskill imports
from buskill.utils import COMMANDS

# subprocess imports
import subprocess
def shutdown(hard: bool) -> None:
    '''
    Shutdown the computer.

    :param hard: If set to True, using hard shutdown, else, using soft shutdown
    '''
    cat: str = COMMANDS.CAT
    bash: str = COMMANDS.BASH
    poweroff: str = COMMANDS.POWEROFF
    shutdown: str = COMMANDS.SHUTDOWN

    if hard: # First case : hard shutdown
        # Verify if sysrq is totally enabled
        if subprocess.run([cat, '/proc/sys/kernel/sysrq'], capture_output=True, text=True).stdout == '1':
            try:
                subprocess.run([bash, '-c', 'echo o > /proc/sysrq-trigger'], check=True) # Try to hard shutdown with sysrq
            except: # In case that didn't work (very unlikely), fallback to other shutdown system
                try:
                    subprocess.run([poweroff, '--no-sync', '--no-wall', '--force'], check=True) # Try to shutdown using poweroff, cuting the power of the computer
                except:
                    try:
                        subprocess.run([shutdown, '-h', '--no-wall', 'now'], check=True) # Try to shutdown and bypass verifications
                    except:
                        subprocess.run([shutdown, '-h', 'now']) # Fallback to soft shutdown
        else:
            try:
                subprocess.run([poweroff, '--no-sync', '--no-wall', '--force'], check=True) # Try to shutdown using poweroff, cuting the power of the computer
            except:
                try:
                    subprocess.run([shutdown, '-h', '--no-wall', 'now'], check=True) # Try to shutdown and bypass verifications
                except:
                    subprocess.run([shutdown, '-h', 'now']) # Fallback to soft shutdown
    else:
        subprocess.run([shutdown, '-h', 'now']) # Soft shutdown