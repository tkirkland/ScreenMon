#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import subprocess
import sys
import threading
import time

from gi.repository import GLib
from pydbus import SessionBus


def screen_lock_handler(locked):
    if locked:
        turn_off_secondary_display()
    # else:
    # You can add actions to be performed when the screen is unlocked


def execute_command(command):
    cmd_result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if cmd_result.returncode != 0:
        print("Execution of: \"%s\" returned non-zero result: %s", command, cmd_result.returncode)
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


def verify_parsed_elements(parsed_elements):
    pass


def get_current_display_setup():
    """
    TODO:
    - Grab IO output from xrandr stdout text, parse and
    - Used parsed elements to determine current display parameters
    - Build a simple text I/O to verify parsed elements before generating
    - A display configuration
    """
    print("Getting current display setup...")
    xrandr_output = subprocess.check_output(["xrandr"]).decode("utf-8")

    # Parse the xrandr output
    # parsed_elements = parse_xrandr_output(xrandr_output)

    # Verify the parsed elements using a simple text I/O
    # verify_parsed_elements(parsed_elements)


def turn_off_secondary_display():
    subprocess.run(["xrandr", "--output", "DP-2", "--off"])


def configure_displays():
    subprocess.run(["xrandr", "--output", "DP-4", "--mode", "3840x2160", "--rate", "120", "--scale", "1x1",
                    "--output", "DP-2", "--mode", "2560x1440", "--rate", "165", "--scale", "1.5x1.5",
                    "--right-of", "DP-4", "--pos", "3840x360", "--primary"])
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
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", action="store_true", help="Get current display setup")
    args = parser.parse_args()

    if args.config:
        get_current_display_setup()

    listen_for_lock_signals()

    # Main loop to check display status
    while True:
        check_display_status()
        time.sleep(1)


if __name__ == "__main__":
    # generate test code for execute_command
    text = execute_command("xrandr")
    print(text)
    exit(0)
    main()
