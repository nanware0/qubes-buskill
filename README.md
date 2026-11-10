# qubes-buskill

> This project isn't finished yet, and the core is in documentation and [specification](./specification.md) process. Also, some module aren't finished at all or need modifications.

## Short presentation

This repository stores the python package that contains the core logic of a BusKill package for Qubes OS.  

### What's BusKill?

BusKill is a Dead Man Switch triggered when a magnetic breakaway is tripped, severing a USB connection. And using some software, we are able to activate some actions when BusKill is triggered. BusKill hardware is licensed under CC-BY-SA, so it's open source. For more information, go to the [BusKill website](https://www.buskill.in/).

### What's the utility of this package?

For a long time, BusKill had no package for Qubes OS, and users had to manually configure BusKill by copying shell scripts, and this solution wasn't really flexible. Actually, there is [an other BusKill contrib package](https://github.com/BusKill/buskill-qubes-contrib/), officially supported by the BusKill team, but this is a minimal package with basic functionnalities. It's good, but doesn't support multiple USB qubes or dom0 as a USB Qube (don't do that but still), and you might want to get your laptop back if he's stole, and not just destroy your data or shutdown your laptop. Also, this other package use shell, which is not a very good solution for long term packages.  
These are the reasons why this package exist: to provide a more complete package that will have more usecases.

## What are the functionnalities?

### Shutdown

- **Soft shutdown:** graceful shutdown of the computer.
- **Hard shutdown:** hard shutdown of the computer, note that there is a known bug with the hard shutdown on Qubes OS, making it takes a long time before shutting down. The hard shutdown can cause data corruption.

### Reboot

- **Soft reboot:** graceful reboot of the computer.
- **Hard reboot:** immediate hard reboot of the computer. The hard reboot can cause data corruption.

### Self-destruct

It erases the LUKS headers of every LUKS devices found, then suspend LUKS, and finally hard shutdown.

**What are the effects?**  
The data are made inaccessible, so you cannot recover them.

**Some limitations?**  
The data aren't really erased, so it's possible to get them in theory, but it's very expensive:  
- *By brutforce:* it will likely not work (else the attackers are really lucky).
- *Using a cryptographic vulnerability:* if there was a cryptographic vulnerability in LUKS or in the cipher function that your LUKS uses (default is AES), the attacker will be able to access your data, but that will not be the main concern and a vulnerability like that is more speculative than a real threat.
- *By physically analyzing the disk:*, the attackers might be able to recover the headers (that's possible in theory), but then, they'll need to extract the passphrase from you so they can access your data, so the self-destruct will act as a simple shutdown.

But don't worry: all these methods are really expensive and not sure to success at all, so your data will not be accessible in real cases.

### Lock screen

This will lock your screen so the attackers cannot easily access your computer. This will not protect you against an attacker with determination and sufficiant time.

### Alarm

This will lock the screen but also activate an alarm (using a [sawtooth wave](https://en.wikipedia.org/wiki/Sawtooth_wave)). This is intended to dissuade thefts to steal your laptop and to alarm you.

### Fallback

When locking your screen or activating an alarm, you might want to also protect your data, that's the reason the fallback system exists: it allows you to setup a fallback for the functionnalities that doesn't shutdown/reboot your computer (aka lock screen and alarm), so that if you weren't able to get your laptop back, one of the data protection functionnalities will be activated and your data will be protected.

### "Recover"

*This functionnality is not a data recovery functionnality.*  
It is intended to display a custom screen with the information that the user gave. It is optionnal, and works with the lock screen and the alarm functionnalities.
> It has not been implemented yet.

## License

Copyright (C) 2020-2026 Michael Altfield, Nanware and the BusKill Team

The contents of this repo are under the GPL version 3 or later. In addition, any content other than code can also be used, at your choice, under CC-BY-SA version 4.0.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.

## General information

### Installation

This repository is a python package, so to install it, you'll need to use `pip`, that will build it automatically (you'll have to specify the path to the package). Note that the stub files are auto generated.

### Roadmap and advancement

You can see a roadmap and the advancement specific to this repository in the file [advancement.md](./advancement.md). For the whole project, you'll get it in the [documentation repository](https://github.com/nanware0/qubes-buskill-doc/).

### Statistics

Using `cloc --exclude-dir=venv,env,.venv,__pycache__,.git,.pytest_cache,.egg-info,node_modules,dist,build .` in the root of this repository, we get these statistics.
```
-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
Python                          47            437            268           1670
Markdown                         3             54              0             81
TOML                             1              6              0             22
Text                             1              1              0              7
-------------------------------------------------------------------------------
SUM:                            52            498            268           1780
-------------------------------------------------------------------------------
```

### Contributing

See [contributing.md](./contributing.md) to learn how to contribute.

### Author and maintainer

Hello, I'm Nanware and I created and maintain this repository. If you want to know more about me, you can check my profile and my [presentation repository](https://github.com/nanware0/hello-world/).  
If you want to contact me and I don't know you, I recommend to use the issues of my presentation repository, they are made for that and I will not treat them as spam, but you can also reach me using my email <nanware@pm.me> (please, use an encrypted email that works with proton), or using [matrix](https://matrix.to/#/@nanware:matrix.org?action=chat).

### For more information

See the [documentation repository](https://github.com/nanware0/qubes-buskill-doc/).