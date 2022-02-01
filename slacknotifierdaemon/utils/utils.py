import re
import logging
import importlib
import inspect

from slacknotifierdaemon.utils.exceptions import ClassNotFoundException

logger = logging.getLogger("service-factory")


def slice_index(x):
    i = 0
    for c in x:
        if c.isalpha():
            i = i + 1
            return i
        i = i + 1


def upper_first(x: str) -> str:
    """Upper the first letter from the string

    Args:
        x (str): The string to upper

    Returns:
        str: The upper string (eg: from test -> Test)
    """
    i = slice_index(x)
    return x[:i].upper() + x[i:]


def lower_first(x: str) -> str:
    """Lower the first letter from the string

    Args:
        x (str): The string to lower

    Returns:
        str: The lower string (eg: from Test -> test)
    """
    i = slice_index(x)
    return x[:i].lower() + x[i:]


def to_camel_case(snake_str: str) -> str:
    """Convert string from python case to camel case

    Args:
        snake_str (str): The string in python format

    Returns:
        str: The string in camel format (eg: from python_test -> pythonTest)
    """
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def camel_to_snake(name: str) -> str:
    """Convert string from camel case to python case

    Args:
        name (str): The string you want to change

    Returns:
        str: Python string format (eg: from pythonTest -> python_test)
    """
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def load_class(module_path: str, default_module: str, config: dict):
    """Load dynamically class inside a module and instanciate it with the config

    Args:
        module_path (str): The module path used to get the class in python path
        default_module (str): The default module name if we don't have any name in config
        config (dict): A dict for instanciate the class

    Raises:
        ClassNotFoundException: When the class is not found in the module

    Returns:
        [Any]: The instanciated class
    """
    module_name = config.get("name", default_module)
    logger.info(f"Dynamically loading module {module_name}")
    snake_case_module_name = camel_to_snake(module_name)
    class_name = upper_first(module_name)
    message_manager_module = importlib.import_module(
        f"{module_path}.{snake_case_module_name}"
    )

    service_class = None
    for name, obj in inspect.getmembers(message_manager_module, inspect.isclass):
        if name == class_name:
            service_class = obj
            break

    if service_class:
        logger.info(f"Instanciated {class_name}")
        return service_class(**config)
    else:
        raise ClassNotFoundException(f"Class {class_name} not found in {module_name}")
