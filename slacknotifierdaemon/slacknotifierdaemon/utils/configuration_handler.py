from watchdog.events import FileSystemEventHandler

from slacknotifierdaemon.slacknotifierdaemon.configuration_manager import (
    ConfigurationManager,
)
import logging

logger = logging.getLogger("configuration-handler")


class ConfigurationHandler(FileSystemEventHandler):
    def on_modified(self, event):
        super().on_modified(event)
        logger.info("On file modification")
        configuration_manager = ConfigurationManager()
        configuration_manager.load_yaml()
        configuration_manager.load_channels()
