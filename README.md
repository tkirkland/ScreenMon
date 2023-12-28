# DisplayMon

DisplayMon is a Python script designed to monitor screen saver events including session lock and unlock.
It leverages the power of DBus for the interprocess communication.

(still WIP)
## TL;DR
If you don't use Linux and X11, this script will be of no use to you.  Its purpose is to allow per-display settings
(in my case, scaling) to present the effect of same resolution displays on dissimilar screen sizes.
## Table of Contents

- [Requirements](#requirements)
- [Dependencies](#dependencies)
- [Install](#install)
- [ToDo](#todo)
- [History](#history)
- [Thanks](#thanks)

## Requirements

Prior to running this script, make sure you have installed the following dependencies:

- `Python 3`
- `pydbus`
- `xrandr` for display configuration (and X11 inherently, since xrandr has no use in Wayland.  I hope this was assumed.)

To check Python version, please run:

```shell
python --version
```
Don't forget to review the system-level dependencies section for non-Python dependencies instructions.

## Dependencies

The script requires some system level dependencies:

- `python3-gi`
- `python3-gi-cairo`
- `gir1.2-gtk-3.0`

The following Python libraries are needed as well:

- `pydbus`
- `gi.repository`

## Install

On Ubuntu (or derivative), you can install the system dependencies by running:

```shell
sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0
```
## TODO

Add ability via command switch to scan active display settings and store them in a config file
to be used in the script to resolve hardcoded display information that is currently passed to the 
'xrandr' calls.

## HISTORY

I am your standard Linux geek.  I developed my passion for tweaking and modding going back to my childhood.
That said, it bugged my significantly that, given the combinability of KDE on Linux, you could not set scaling
per screen in X11 using Nvidia proprietary drivers.  Combine that with the horrible performance of Nouveau and you
see my dilemma.  I searched for weeks and could find nothing so the idea to make this script was born.  Originally
created as a shell script, I decided to try making a Python variant.  Here we are.

## THANKS
Giving credit where credit is due; Special thanks to user Naftuli Kay in
[this thread.](https://askubuntu.com/questions/631997/subscribe-for-dbus-event-of-screen-power-off)