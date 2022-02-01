from unittest.mock import patch
from slacknotifierdaemon.configuration_manager import (
    DEFAULT_SERVICE,
    SERVICES_PYTHON_PATH,
)
from slacknotifierdaemon.utils.service_factory import ServiceFactory
from phue import Bridge


@patch.object(Bridge, "connect")
@patch.object(Bridge, "get_api")
def test_service_factory(
    mocked_connect_method,
    mocked_get_api_method,
    devices_config_data,
    device_config_data,
):
    mocked_connect_method.return_value = {}
    mocked_get_api_method.return_value = {}
    service_factory = ServiceFactory()
    second_service_old = None
    second_service = None

    for device in devices_config_data:
        service = devices_config_data[device].get("service")
        seconde_service_old = service_factory.build(
            SERVICES_PYTHON_PATH, DEFAULT_SERVICE, service
        )

    assert len(service_factory.services) == 2

    for device in devices_config_data:
        service = devices_config_data[device].get("service")
        second_service = service_factory.build(
            SERVICES_PYTHON_PATH, DEFAULT_SERVICE, service
        )

    assert len(service_factory.services) == 2
    assert second_service is seconde_service_old

    service = device_config_data["arduino"].get("service")
    new_service = service_factory.build(SERVICES_PYTHON_PATH, DEFAULT_SERVICE, service)

    assert len(service_factory.services) == 3
