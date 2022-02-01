from unittest.mock import patch
from slack_sdk import WebClient
from slacknotifierdaemon.configuration_manager import ConfigurationManager
from slacknotifierdaemon.devices.default_device import DefaultDevice
from slacknotifierdaemon.messagemanagers.default_message_manager import (
    DefaultMessageManager,
)
from slacknotifierdaemon.services.arduino_service import (
    ArduinoService,
)
from slacknotifierdaemon.services.philips_hue_service import (
    PhilipsHueService,
)

from phue import Bridge


class FakeApp:
    def __init__(self) -> None:
        self.client = WebClient(token="")


def test_singleton():
    configuration_manager_1 = ConfigurationManager()
    configuration_manager_2 = ConfigurationManager()
    assert configuration_manager_1 == configuration_manager_2


@patch.object(Bridge, "connect")
@patch.object(Bridge, "get_api")
def test_load_devices(
    mocked_connect_method, mocked_get_api_method, devices_config_data
):
    mocked_connect_method.return_value = {}
    mocked_get_api_method.return_value = {}
    configuration_manager = ConfigurationManager()
    modules = configuration_manager.load_devices(devices_config_data)
    assert len(modules) == 2
    assert isinstance(modules[0], DefaultDevice)
    assert isinstance(modules[1], DefaultDevice)
    assert isinstance(modules[0].service, ArduinoService)
    assert isinstance(modules[1].service, PhilipsHueService)


@patch.object(WebClient, "conversations_list")
@patch.object(Bridge, "get_api")
@patch.object(Bridge, "connect")
def test_load_channels(
    mocked_connect_method,
    mocked_get_api_method,
    mocked_conversations_list,
    channels_from_slack_data,
    channels_config_data,
):
    mocked_connect_method.return_value = {}
    mocked_get_api_method.return_value = {}
    mocked_conversations_list.return_value = channels_from_slack_data

    configuration_manager = ConfigurationManager()
    configuration_manager.app = FakeApp()
    configuration_manager.slack_client = configuration_manager.app.client
    configuration_manager.config = channels_config_data

    channels = configuration_manager.load_channels()

    assert len(channels) == 1
    assert channels["test_id1"].name == "test_name1"
    assert channels["test_id1"].description == "test_description"
    assert isinstance(channels["test_id1"].message_manager, DefaultMessageManager)
    assert isinstance(channels["test_id1"].devices[0], DefaultDevice)
    assert isinstance(channels["test_id1"].devices[0].service, ArduinoService)
    assert isinstance(channels["test_id1"].devices[1].service, PhilipsHueService)
