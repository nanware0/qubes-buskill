# qubes-buskill

> This project is still in primary development.

This repository contains the python package for the core logic of a Buskill package for Qubes OS.  
Some repositories will be created in the next days to store the other modules of the dom0 package and the documentation.  
Currently, the alarm system depends from numpy and sounddevice and doesn't support a sys-audio qube, for a stable release, it will directly use pipewire's sockets and will support a sys-audio qube.  

The "recover" functionnality is intended to display a custom screen with the information saved by the user (all the informations are optionnal), so if someone find the laptop and want to give it back, he can. 
