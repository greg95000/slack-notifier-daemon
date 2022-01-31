from cmath import log
from typing import Dict, List
from slack_bolt import App
from yaml import load, Loader
import importlib
import inspect
import logging
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slacknotifierdaemon.slacknotifierdaemon.devices.device_interface import (
    DeviceInterface,
)
from slacknotifierdaemon.slacknotifierdaemon.models.channel import Channel
from slacknotifierdaemon.slacknotifierdaemon.models.user import User
from slacknotifierdaemon.slacknotifierdaemon.utils.singleton_meta import SingletonMeta

from slacknotifierdaemon.slacknotifierdaemon.utils.utils import (
    camel_to_snake,
    upper_first,
)


SERVICES_PYTHON_PATH = "slacknotifierdaemon.slacknotifierdaemon.services"
MESSAGE_MANAGERS_PATH = "slacknotifierdaemon.slacknotifierdaemon.messagemanagers"
DEVICES_PATH = "slacknotifierdaemon.slacknotifierdaemon.devices"

DEFAULT_DEVICE = "defaultDevice"
DEFAULT_MESSAGE_MANAGER = "defaultMessageManager"
DEFAULT_SERVICE = "defaultService"

logger = logging.getLogger("configuration-manager")


class ClassNotFoundException(Exception):
    pass


class ConfigurationManager(metaclass=SingletonMeta):
    def __init__(self, config_path: str = "./config/slack-notifier.yml") -> None:
        self.app = None
        self.config_path = config_path
        self.slack_client = None
        self.channels = {}
        self.user = {}
        self.config = {}

    def load_yaml(self):
        logger.info("Loading configuration file")
        with open(self.config_path, "r") as yaml_file:
            self.config = load(yaml_file, Loader=Loader)
            return self.config

    def load_app(self):
        logger.info("Loading slack client application")
        yaml_config = self.config
        self.app = App(token=yaml_config["bot-token"])
        self.slack_client = self.app.client
        return self.app

    def load_socket(self):
        logger.info("Loading socket handler for slack client")
        yaml_config = self.config
        if self.app:
            self.socket = SocketModeHandler(self.app, yaml_config["app-token"])
            return self.socket
        else:
            raise Exception("App is not instanciated, cannot create the socket")

    def load_user(self) -> User:
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
                    instanciated_message_manager = self.load_module(
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
        instanciated_devices = []
        logger.info("Loading devices")
        for device_name in devices:

            service = devices[device_name].pop("service", {})
            instanciated_service = self.load_module(
                SERVICES_PYTHON_PATH, DEFAULT_SERVICE, service
            )
            instanciated_device = self.load_module(
                DEVICES_PATH, DEFAULT_DEVICE, devices[device_name]
            )
            instanciated_device.service = instanciated_service
            instanciated_devices.append(instanciated_device)

        return instanciated_devices

    def load_module(self, module_path, default_module, config):
        module_name = config.pop("name", default_module)
        logger.info(f"Dynamically loading module {module_name}")
        snake_case_module_name = camel_to_snake(module_name)
        class_name = upper_first(module_name)
        message_manager_module = importlib.import_module(
            f"{module_path}.{snake_case_module_name}"
        )

        service_class = None
        for name, obj in inspect.getmembers(message_manager_module, inspect.isclass):
            if name == class_name:
                service_class = obj
                break

        if service_class:
            logger.info(f"Instanciated {class_name}")
            return service_class(**config)
        else:
            raise ClassNotFoundException(
                f"Class {class_name} not found in {module_name}"
            )
