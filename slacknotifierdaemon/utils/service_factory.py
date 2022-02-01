import logging
from slacknotifierdaemon.services.service_interface import ServiceInterface
from slacknotifierdaemon.utils.utils import load_class, upper_first

logger = logging.getLogger("service-factory")


class ServiceFactory:
    """The ServiceFactory help us to create the services and manage when we want to use the same service from differents channels"""

    def __init__(self) -> None:
        self.services = []

    def build(self, module_path, default_module, config) -> ServiceInterface:
        module_name = config.get("name", default_module)
        class_name = upper_first(module_name)
        logger.info(f"Building class {class_name}")

        if self.services:
            for service in self.services:
                if service[0] == class_name and service[1] == config:
                    return service[2]

        instanciated_service = load_class(module_path, default_module, config)
        self.services.append((class_name, config, instanciated_service))
        return instanciated_service
