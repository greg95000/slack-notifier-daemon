from slacknotifierdaemon.slacknotifierdaemon.devices.device_interface import (
    DeviceInterface,
)


class DefaultDevice(DeviceInterface):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
