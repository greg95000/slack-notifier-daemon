from typing import List
from slacknotifierdaemon.devices.device_interface import (
    DeviceInterface,
)
from slacknotifierdaemon.messagemanagers.default_message_manager import (
    DefaultMessageManager,
)
from slacknotifierdaemon.messagemanagers.message_manager_interface import (
    MessageManagerInterface,
)


class Channel:
    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        devices: List[DeviceInterface],
        message_manager: MessageManagerInterface = DefaultMessageManager({}),
    ) -> None:
        self._id = id
        self._name = name
        self.description = description
        self.devices = devices
        self.message_manager = message_manager

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name
