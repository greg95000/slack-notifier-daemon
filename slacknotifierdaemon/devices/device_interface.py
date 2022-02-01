from slacknotifierdaemon.services.service_interface import (
    ServiceInterface,
)
from slacknotifierdaemon.services.default_service import (
    DefaultService,
)


class DeviceInterface:
    def __init__(
        self,
        name: str = "",
        service: ServiceInterface = DefaultService(),
    ) -> None:
        """Init for device interface

        Args:
            name (str, optional): The name of the device. Defaults to "".
            service (ServiceInterface, optional): The service attached to the device. Defaults to DefaultService().
        """
        self.name = name
        self.service = service
