from slacknotifierdaemon.slacknotifierdaemon.services.service_interface import (
    ServiceInterface,
)
from slacknotifierdaemon.slacknotifierdaemon.services.default_service import (
    DefaultService,
)


class DeviceInterface:
    def __init__(
        self,
        name: str = "",
        service: ServiceInterface = DefaultService(),
    ) -> None:
        self.name = name
        self.service = service
