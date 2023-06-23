from ._time import _manage_time, TIME

import io


def _property_slots():
    return "layer", "scale", "x", "y", "start_time", "delete_time", "delay"  # The latter three properties are
    # eventually going to be defunct.


def _replace_by_variables(value, constants):
    constant_type_list = [
        constants.address,
        constants.bool,
        constants.float,
        constants.int,
        constants.string
    ]

    for constant_type in constant_type_list:
        value = _loop_over_type(value, constant_type)
    return value


def _loop_over_type(value, constants):
    for name in dir(constants):
        if name.startswith("__") or name.endswith("__"):
            continue
        value = value.replace(f"${name}", str(constants.get_variable(name)))
    return value


class Originals:
    __slots__ = _property_slots()

    def get_property(self, name):
        return self.__getattribute__(name)

    def set_property(self, name, value):
        self.__setattr__(name, value)


class Properties:
    __slots__ = (*_property_slots(), "_original", "_variables_access")

    file_name: str
    layer: int
    scale: float
    x: int
    y: int
    start_time: TIME
    delete_time: TIME
    delay: TIME

    def __init__(self):
        self._variables_access = None

    def __repr__(self):
        string = io.StringIO(f"{self.__class__.__name__}(")
        first = True
        last = False
        for k, v in dir(self):
            if k.startswith("__") or k.endswith("__"):
                continue
            if not first and not last:
                string.write(", ")
            string.write(f"{k}={v}")
            first = False
        string.write(")")
        return string.getvalue()

    def add_property(self, name, value):
        value = self.validate_property(name, value)
        if name[0:4] == "move":
            if not hasattr(self, name):
                self.__setattr__(name, [value])
            else:
                getattr(self, name).append(value)
            return
        self.__setattr__(name, value)

    def get_property(self, name):
        return self.__getattribute__(name)

    def init_variables_instance(self, variables):
        self._variables_access = variables

    def validate_property(self, name, value):
        value = _replace_by_variables(value, self._variables_access.constants)
        annotation = self.__annotations__[name]
        if annotation == TIME:
            value = _manage_time(value, self._variables_access.metadata.frame_rate)
        else:
            value = annotation(value)
        return value
