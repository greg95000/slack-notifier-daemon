from cmath import log
from typing import Dict, List
from slack_bolt import App
from yaml import load, Loader

import logging
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slacknotifierdaemon.devices.device_interface import (
    DeviceInterface,
)
from slacknotifierdaemon.models.channel import Channel
from slacknotifierdaemon.models.user import User
from slacknotifierdaemon.utils.service_factory import ServiceFactory
from slacknotifierdaemon.utils.singleton_meta import SingletonMeta

from slacknotifierdaemon.utils.utils import load_class


SERVICES_PYTHON_PATH = "slacknotifierdaemon.services"
MESSAGE_MANAGERS_PATH = "slacknotifierdaemon.messagemanagers"
DEVICES_PATH = "slacknotifierdaemon.devices"

DEFAULT_DEVICE = "defaultDevice"
DEFAULT_MESSAGE_MANAGER = "defaultMessageManager"
DEFAULT_SERVICE = "defaultService"

logger = logging.getLogger("configuration-manager")


class ConfigurationManager(metaclass=SingletonMeta):
    """The configuration manager is a configuration loader. It load the yaml file and instanciate everything that the application needs

    Args:
        metaclass ([type], optional): The singleton metaclass as the configurationManager is the core of the application. Defaults to SingletonMeta.
    """

    def __init__(self, config_path: str = "./config/slack-notifier.yml") -> None:
        """Init the ConfigurationManager

        Args:
            config_path (str, optional): The configuration file path to load. Defaults to "./config/slack-notifier.yml".
        """
        self.app = None
        self.config_path = config_path
        self.slack_client = None
        self.channels = {}
        self.user = {}
        self.config = {}

    def load_yaml(self):
        """Load the yaml configuration file

        Returns:
            [dict]: The configuration parsed dict
        """
        logger.info("Loading configuration file")
        with open(self.config_path, "r") as yaml_file:
            self.config = load(yaml_file, Loader=Loader)
            return self.config

    def load_app(self):
        """Load the application for slack bolt to consume the sockets and call with HTTP via the API

        Returns:
            [slack_bolt.App]: The application
        """
        logger.info("Loading slack client application")
        yaml_config = self.config
        self.app = App(token=yaml_config["bot-token"])
        self.slack_client = self.app.client
        return self.app

    def load_socket(self):
        """Load the websocket used for the slack bot

        Raises:
            Exception: If the application is not instanciated as it is a requirement to load the socket

        Returns:
            [slack_bolt.adapter.socket_mode.SocketModeHandler]: The websocket handler
        """
        logger.info("Loading socket handler for slack client")
        yaml_config = self.config
        if self.app:
            self.socket = SocketModeHandler(self.app, yaml_config["app-token"])
            return self.socket
        else:
            raise Exception("App is not instanciated, cannot create the socket")

    def load_user(self) -> User:
        """Load the user from the slack API

        Raises:
            Exception: If the application is not instanciated as it is a requirement to load the data

        Returns:
            User: The user class that contains the username and the id
        """
        logger.info("Loading user information")
        yaml_config = self.config
        username = yaml_config["username"]
        if not self.app:
            raise Exception("App is not instanciated, cannot load the user")
        users = self.slack_client.users_list()

        for user in users.get("members", []) or []:
            if username == user["name"]:
                self.user = User(user["id"], username)
                return self.user
        return None

    def load_channels(self) -> Dict[str, Channel]:
        """Load all the channels and the configuration (services, devices, ...)

        Raises:
            Exception: If the app is not instanciated we can't load the data

        Returns:
            Dict[str, Channel]: The dict with the channel id and the channel object
        """
        logger.info("Loading channels")
        if not self.app:
            raise Exception("App is not instanciated, cannot load channels")

        channels_by_api = self.slack_client.conversations_list()
        yaml_config = self.config
        channels_config = yaml_config["channels"]

        for channel_config_key in channels_config:
            for channel_by_api in channels_by_api.get("channels", []) or []:

                if (
                    channel_by_api["is_channel"]
                    and channel_config_key == channel_by_api["name"]
                ):
                    channel_id = channel_by_api["id"]
                    channel_name = channel_by_api["name"]
                    description = channel_by_api["purpose"]["value"]
                    devices = channels_config[channel_config_key].get("devices", {})
                    message_manager = channels_config[channel_config_key].get(
                        "message-manager", {}
                    )

                    instanciated_devices = self.load_devices(devices)
                    instanciated_message_manager = load_class(
                        MESSAGE_MANAGERS_PATH, DEFAULT_MESSAGE_MANAGER, message_manager
                    )
                    instanciated_channel = Channel(
                        channel_id,
                        channel_name,
                        description,
                        instanciated_devices,
                        instanciated_message_manager,
                    )
                    self.channels[channel_id] = instanciated_channel
        return self.channels

    def load_devices(self, devices: dict = {}) -> List[DeviceInterface]:
        """Load all devices from a channel with their services

        Args:
            devices (dict, optional): The devices configuration dict to parse and load. Defaults to {}.

        Returns:
            List[DeviceInterface]: The list of the devices
        """
        instanciated_devices = []
        logger.info("Loading devices")
        service_factory = ServiceFactory()
        for device_name in devices:

            service = devices[device_name].pop("service", {})
            instanciated_service = service_factory.build(
                SERVICES_PYTHON_PATH, DEFAULT_SERVICE, service
            )
            instanciated_device = load_class(
                DEVICES_PATH, DEFAULT_DEVICE, devices[device_name]
            )
            instanciated_device.service = instanciated_service
            instanciated_devices.append(instanciated_device)

        return instanciated_devices
