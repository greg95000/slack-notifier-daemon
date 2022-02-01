#!/usr/bin/env python

import atexit

from slack_bolt import App
from slacknotifierdaemon.configuration_manager import (
    ConfigurationManager,
)
from watchdog.observers import Observer
from slacknotifierdaemon.utils.configuration_handler import (
    ConfigurationHandler,
)
import time
import psutil
import daemon
import sys


def exit_handler():
    """Exit the application and turn off all the devices with the off method"""
    print("In exit handler")
    configuration_manager = ConfigurationManager()
    channels = configuration_manager.channels
    for channel in channels:
        for device in channels[channel].devices:
            off_funct = getattr(device.service, "off", None)
            if callable(off_funct):
                off_funct()


def register_listeners(app: App):
    @app.event("message")
    def read_message(event, say):
        """Read the slack message and parse it to execute on device

        Args:
            event (dict): the message event
            say ([type]): [description]
        """
        configuration_manager = ConfigurationManager()
        channel = configuration_manager.channels.get(event["channel"])
        user = configuration_manager.user
        if channel:
            status = channel.message_manager.parse_message(event["text"])
            for device in channel.devices:
                device.service.run(status, user)
        exit(0)


def start():
    """Start all the requirement for the application"""
    configuration_manager = ConfigurationManager()
    socket = configuration_manager.load_socket()
    configuration_manager.load_user()
    configuration_manager.load_channels()
    socket.connect()


def main():
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    else:
        config_path = "./config/slack-notifier.yml"

    configuration_manager = ConfigurationManager(config_path)
    configuration_manager.load_yaml()
    app = configuration_manager.load_app()
    register_listeners(app)
    start()

    atexit.register(exit_handler)
    event_handler = ConfigurationHandler()
    observer = Observer()
    observer.schedule(event_handler, config_path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()


# Start your app
if __name__ == "__main__":
    main()
