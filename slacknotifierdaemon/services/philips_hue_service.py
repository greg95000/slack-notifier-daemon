from phue import Bridge
from rgbxy import Converter

from slacknotifierdaemon.services.service_interface import (
    ServiceInterface,
)


class PhilipsHueService(ServiceInterface):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.bridge = Bridge(ip=kwargs.get("ip_address", ""))
        self.bridge.get_api()
        self.converter = Converter()
        self.status = kwargs.get("status")
        self.lamps = kwargs.get("lamps")

    def run(self, status, user=None):
        status = self.status.get(status)
        if status:
            hex_color = "{:x}".format(status["color"])
            xy_color = self.converter.hex_to_xy(hex_color)
            command = {"on": True, "xy": xy_color}
            self.bridge.set_light(self.lamps, command)

    def off(self):
        command = {"on": False}
        self.bridge.set_light(self.lamps, command)
