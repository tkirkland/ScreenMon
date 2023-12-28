# SessionMon

SessionMon is a Python script designed to monitor screen saver events including session lock and unlock. It leverages the power of DBus for the interprocess communication.

(still WIP)
## Table of Contents

- [Requirements](#requirements)

## Requirements

Prior to running this script, make sure you have installed the following dependencies:

- `Python 3`
- `pydbus`

To check Python version, please run:

```shell
python --version
```

Don't forget to review the system-level dependencies section for non-Python dependencies instructions.

## System-Level Dependencies

It might require some system level dependencies:

- `glib-2.0`
- `dbus-1`

On Ubuntu, you can install them by running:

```shell
sudo apt-get install libglib2.0-dev install libdbus-1-dev
```