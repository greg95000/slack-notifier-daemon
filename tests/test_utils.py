from slacknotifierdaemon.configuration_manager import (
    DEFAULT_DEVICE,
    DEFAULT_MESSAGE_MANAGER,
    DEFAULT_SERVICE,
    DEVICES_PATH,
    MESSAGE_MANAGERS_PATH,
    SERVICES_PYTHON_PATH,
)
from slacknotifierdaemon.devices.default_device import DefaultDevice
from slacknotifierdaemon.messagemanagers.default_message_manager import (
    DefaultMessageManager,
)
from slacknotifierdaemon.services.default_service import DefaultService
from slacknotifierdaemon.utils.utils import (
    camel_to_snake,
    load_class,
    lower_first,
    to_camel_case,
    upper_first,
)


def test_load_class(service_config_empty_data):
    module = load_class(
        SERVICES_PYTHON_PATH, DEFAULT_SERVICE, service_config_empty_data
    )
    assert isinstance(module, DefaultService)


def test_load_message_manage_default(service_config_empty_data):
    module = load_class(
        MESSAGE_MANAGERS_PATH, DEFAULT_MESSAGE_MANAGER, service_config_empty_data
    )
    assert isinstance(module, DefaultMessageManager)


def test_load_device_default(service_config_empty_data):
    module = load_class(DEVICES_PATH, DEFAULT_DEVICE, service_config_empty_data)
    assert isinstance(module, DefaultDevice)


def test_load_service_default(service_config_empty_data):
    module = load_class(
        SERVICES_PYTHON_PATH, DEFAULT_SERVICE, service_config_empty_data
    )
    assert isinstance(module, DefaultService)


def test_upper_first():
    upper_string_value = upper_first("test")
    assert upper_string_value == "Test"


def test_lower_first():
    lower_string_value = lower_first("Test")
    assert lower_string_value == "test"


def test_to_camel_case():
    camel_case_value = to_camel_case("test_python")
    assert camel_case_value == "testPython"


def test_camel_to_snake():
    snake_case_value = camel_to_snake("testPython")
    assert snake_case_value == "test_python"
