import re


def slice_index(x):
    i = 0
    for c in x:
        if c.isalpha():
            i = i + 1
            return i
        i = i + 1


def upper_first(x: str) -> str:
    i = slice_index(x)
    return x[:i].upper() + x[i:]


def lower_first(x: str) -> str:
    i = slice_index(x)
    return x[:i].lower() + x[i:]


def to_camel_case(snake_str):
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


def camel_to_snake(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()
