#!/usr/bin/env python

import atexit
from slacknotifierdaemon.slacknotifierdaemon.configuration_manager import (
    ConfigurationManager,
)
from watchdog.observers import Observer
from slacknotifierdaemon.slacknotifierdaemon.utils.configuration_handler import (
    ConfigurationHandler,
)
import time

configuration_manager = ConfigurationManager()
configuration_manager.load_yaml()
app = configuration_manager.load_app()

import os
import psutil

path = os.path.abspath(__file__)


def exit_handler():
    print("In exit handler")
    channels = configuration_manager.channels
    for channel in channels:
        for device in channels[channel].devices:
            off_funct = getattr(device.service, "off", None)
            if callable(off_funct):
                off_funct()


@app.event("message")
def read_message(event, say):
    channel = configuration_manager.channels.get(event["channel"])
    user = configuration_manager.user
    if channel:
        status = channel.message_manager.parse_message(event["text"])
        for device in channel.devices:
            device.service.run(status, user)
    exit(0)


def start():
    socket = configuration_manager.load_socket()
    configuration_manager.load_user()
    configuration_manager.load_channels()
    socket.connect()


def main():
    start()


# Start your app
if __name__ == "__main__":
    atexit.register(exit_handler)
    main()
    event_handler = ConfigurationHandler()
    observer = Observer()
    observer.schedule(event_handler, "./config/", recursive=True)
    observer.start()
    try:
        while True:
            print(psutil.Process().memory_info().rss / (1024 * 1024))
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
