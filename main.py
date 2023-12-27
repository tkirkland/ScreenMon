#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
import dbus
import logging
import sys

DBUS_INTERFACE: str = "org.freedesktop.DBus.Properties"


class ScreenSaverEventListener(object):
    """
    Initializes an instance of the class.

    Parameters:
        None

    Returns:
        None
    """
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._mainloop = DBusGMainLoop()
        self._loop = GLib.MainLoop()
        self._session_bus = dbus.SessionBus(mainloop=self._mainloop)
        self._receiver_args, self._receiver_kwargs = None, None

    def _setup(self):
        self._receiver_args = (self._on_session_activity_change,)
        self._receiver_kwargs = dict(dbus_interface=DBUS_INTERFACE, path="/org/gnome/SessionManager",
                                     signal_name="PropertiesChanged",
                                     sender_keyword="sender", destination_keyword="dest",
                                     interface_keyword="interface", member_keyword="member", path_keyword="path",
                                     message_keyword="message")
        self._session_bus.add_signal_receiver(*self._receiver_args, **self._receiver_kwargs)

    def _on_session_activity_change(self, target: dbus.String, changed_properties: dbus.Dictionary, *args, **kwargs):
        if target != "org.gnome.SessionManager" or changed_properties.get("SessionIsActive") is None:
            return
        self._on_session_unlock() if changed_properties.get("SessionIsActive") else self._on_session_lock()

    def _on_session_lock(self):
        self._logger.info("Session Locked")

    def _on_session_unlock(self):
        self._logger.info("Session Unlocked")

    def _run(self):
        self._logger.debug("Starting event loop.")
        self._loop.run()

    def _shutdown(self):
        self._logger.debug("Stopping event loop.")
        self._session_bus.remove_signal_receiver(*self._receiver_args, **self._receiver_kwargs)
        self._loop.quit()


def setup_logging():
    console = logging.StreamHandler(sys.stderr)
    console.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)-5s] %(name)s: %(message)s", datefmt="%Y-%m-%dT%H:%M:%S%z"))
    logging.addLevelName(logging.WARNING, "WARN")
    logging.getLogger().addHandler(console)
    logging.getLogger().setLevel(logging.DEBUG)


def main():
    setup_logging()
    listener = ScreenSaverEventListener()
    listener._setup()
    try:
        listener._run()
    except KeyboardInterrupt:
        sys.stderr.write("ctrl+c received, shutting down...\n")
        listener._shutdown()


if __name__ == "__main__":
    main()
