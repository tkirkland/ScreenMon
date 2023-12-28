# DisplayMon

SessionMon is a Python script designed to monitor screen saver events including session lock and unlock.
It leverages the power of DBus for the interprocess communication.

(still WIP)
## Table of Contents

- [Requirements](#requirements)
- [Dependencies](#dependencies)
- [Install](#install)

## Requirements

Prior to running this script, make sure you have installed the following dependencies:

- `Python 3`
- `pydbus`

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

## The following Python libraries are needed as well:

- `pydbus`
- 
## Install

On Ubuntu, you can install them by running:

```shell
sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0
```