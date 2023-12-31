#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import subprocess
import sys
import threading
import time

from gi.repository import GLib
from pydbus import SessionBus
from screeninfo import get_monitors


def which(program):
    def is_executable(file_path):
        return os.path.isfile(file_path) and os.access(file_path, os.X_OK)

    _fp, _fn = os.path.split(program)
    if _fp:
        if is_executable(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            executable_file = os.path.join(path, program)
            if is_executable(executable_file):
                return executable_file
    return None


def screen_lock_handler(locked):
    if locked:
        turn_off_secondary_display()
    # else:
    # You can add actions to be performed when the screen is unlocked


def execute_command(command):
    cmd_result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if cmd_result.returncode != 0:
        print(f"Execution of: {command} failed with return code {cmd_result.returncode}")
        sys.exit(1)
    return cmd_result.stdout.splitlines()


def listen_for_lock_signals():
    """
    Listens for lock signals and runs the listen function in a separate thread.

    This function sets up a listener for lock signals by connecting to the ActiveChanged signal of the
    ScreenSaver D-Bus service. It then starts the listener function in a separate thread.
    """
    def listen():
        bus = SessionBus()
        screensaver = bus.get(".ScreenSaver")  # Adjust this as per your D-Bus service
        screensaver.ActiveChanged.connect(screen_lock_handler)
        loop = GLib.MainLoop()
        loop.run()

    # Run the listen function in a separate thread
    listener_thread = threading.Thread(target=listen, daemon=True)
    listener_thread.start()


def get_current_display_setup():
    monitors = []
    for display in get_monitors():
        name = display.name
        is_prim = display.is_primary  # Assuming that 'is_primary' is a property of a display
        x = display.width  # Assuming that 'width' is a property of a display
        y = display.height  # Assuming that 'height' is a property of a display
        monitors.append(Monitor(name, is_prim, x, y))
    return monitors


class Monitor:
    def __init__(self, name, is_prim, x, y):
        self.name = name
        self.is_prim = is_prim
        self._x = x  # Private attribute for storing x value
        self._y = y  # Private attribute for storing y value

    @property
    def x(self):
        return self._x  # Accessor for x

    @property
    def y(self):
        return self._y  # Accessor for y


def turn_off_secondary_display():
    # subprocess.run(["xrandr", "--output", "DP-2", "--off"])
    execute_command("xrandr --output DP-2 --off)")


def configure_displays():
    execute_command(
        "xrandr --output DP-4 --mode 3840x2160 --rate 120 --scale 1x1 \
        --output DP-2 --mode 2560x1440 --rate 165 --scale 1.5x1.5 \
        --right-of DP-4 --pos 3840x360 --primary"
    )
    # subprocess.run(["xrandr", "--output", "DP-4", "--mode", "3840x2160", "--rate", "120", "--scale", "1x1",
    #                 "--output", "DP-2", "--mode", "2560x1440", "--rate", "165", "--scale", "1.5x1.5",
    #                 "--right-of", "DP-4", "--pos", "3840x360", "--primary"])
    # we run again to force wallpaper resize  TODO: less kludge way yo achieve?
    subprocess.run(
        ["xrandr", "--output", "DP-4", "--mode", "3840x2160", "--rate", "120", "--scale", "1x1", "--primary"])


def check_display_status():
    """
    Check the display status by running the 'xrandr' command and capture its output. If the output contains the
    string 'DP-2 connected' and an asterisk '*', call the 'configure_displays()' function. This function does not
    take any parameters and does not return any value.
    """
    result = subprocess.run(["xrandr"], capture_output=True, text=True)
    if 'DP-2 connected' in result.stdout and '*' in result.stdout.split('DP-2 connected')[1].split('\n')[0]:
        configure_displays()


def main():
    if which("xrandr") is None:
        print("xrandr command not found. Please install xrandr.")
        sys.exit(1)
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", action="store_true", help="Get current display setup")
    args = parser.parse_args()

    if args.config:
        # Call the function to get the list of monitors
        displays = get_current_display_setup()
        # Iterate through each monitor in the list
        for monitor in displays:
            print(f"DEVICE: {monitor.name} [{monitor.x}x{monitor.y}] {'(PRIMARY)' if monitor.is_prim else ''}")
        print(f"\nFound {len(displays)} {'displays.' if len(displays) > 1 else 'display.'}")
    listen_for_lock_signals()

    try:
        while True:
            check_display_status()
            time.sleep(1)
    except KeyboardInterrupt:
        print("KEYBOARD INTERRUPT")
        sys.exit(0)


if __name__ == "__main__":
    main()
