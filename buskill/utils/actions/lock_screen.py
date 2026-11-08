# The package policy is that every step must be commented 
# and that documenting the code is an obligation, 
# don't be afraid by the comments,
# they're here to specify the expected behavior

# buskill imports
from buskill.utils import COMMANDS

# subprocess imports
import subprocess

# os imports
import os

def lock_screen() -> bool:
    '''
    Universal screen locker.
    '''
    try:
        subprocess.run([COMMANDS.LOGINCTL, 'lock-session'], check=True) # Try to lock the screen with systemd
        return True # Return True if the lock worked
    except: # If the command failed for an other reason
        desktop: str = os.getenv('XDG_CURRENT_DESKTOP', '').lower() # Get the current desktop
        commands: dict[str, list[list[str]]] = {
            'kde': [[COMMANDS.QDBUS, 'org.freedesktop.ScreenSaver', 'Lock']], # KDE screenlocker commands
            'xfce': [[COMMANDS.XFCE4_SCREENSAVER_COMMAND, '--lock'], [COMMANDS.XFLOCK4]], # XFCE screenlocker commands
            'i3': [[COMMANDS.I3LOCK], [COMMANDS.SLOCK]], # i3 screenlocker commands
            'awesome': [[COMMANDS.I3LOCK], [COMMANDS.SLOCK]] # AwesomeWM screenlocker commands
        } # List of commands for every Qubes OS Desktop

        for env, cmds in commands.items(): # Iterate on the desktops
            if env in desktop: # Test if the desktop is the current desktop
                for cmd in cmds: # Iterate on the commands of the desktop
                    try:
                        subprocess.run(cmd, check=True) # Try to lock the screen with the current command
                        return True # Return True if the lock worked
                    except: continue # Continue if the command didn't worked

    return False # Return False if we failed to lock the screen