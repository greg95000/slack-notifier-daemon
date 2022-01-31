from slacknotifierdaemon.slacknotifierdaemon.services.service_interface import (
    ServiceInterface,
)


class DefaultService(ServiceInterface):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
