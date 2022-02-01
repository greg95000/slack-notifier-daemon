from slacknotifierdaemon.services.service_interface import (
    ServiceInterface,
)


class ArduinoService(ServiceInterface):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def run(self, status, user=None):
        return ""
