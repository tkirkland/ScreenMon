#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydbus import SessionBus
from gi.repository import GLib
import threading
import subprocess
import sys
import time
import argparse


def screen_lock_handler(locked):
    if locked:
        turn_off_dp2()
    # else:
        # You can add actions to be performed when the screen is unlocked


def listen_for_lock_signals():
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
    print("Getting current display setup...")
    # Your code to get the display setup goes here


def turn_off_dp2():
    subprocess.run(["xrandr", "--output", "DP-2", "--off"])


def configure_displays():
    subprocess.run(["xrandr", "--output", "DP-4", "--mode", "3840x2160", "--rate", "120", "--scale", "1x1",
                    "--output", "DP-2", "--mode", "2560x1440", "--rate", "165", "--scale", "1.5x1.5",
                    "--right-of", "DP-4", "--pos", "3840x360", "--primary"])
    subprocess.run(
        ["xrandr", "--output", "DP-4", "--mode", "3840x2160", "--rate", "120", "--scale", "1x1", "--primary"])


def check_display_status():
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
    main()
