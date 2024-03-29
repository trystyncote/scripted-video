from scripted_video.objects._time import _manage_time, TIME

import io
from pathlib import Path


def _property_slots():
    return "file_name", "layer", "scale", "x", "y", "start_time", "delete_time", "delay"  # The latter three properties
    # are eventually going to be defunct.


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

    file_name: Path
    layer: int
    scale: float
    x: int
    y: int
    start_time: TIME
    delete_time: TIME
    delay: TIME

    def __init__(self, variables_instance):
        self._variables_access = variables_instance

    def __repr__(self):
        existing_attr = [slots_attr for slots_attr in self.__slots__
                         if hasattr(self, slots_attr) and slots_attr != "_variables_access"]
        if not existing_attr:
            return f"{self.__class__.__name__}()"
        string = io.StringIO()
        string.write(f"{self.__class__.__name__}(")
        last_element = existing_attr[-1]
        for attr_name in existing_attr:
            attr_value = getattr(self, attr_name)
            if attr_name == "file_name":
                string.write(f"{attr_name}={attr_value.__class__.__name__}(...")
                for i, n in enumerate(attr_value.parts[-3:]):
                    string.write(n)
                    if i != 2:
                        string.write("/")
                string.write(")")
            else:
                string.write(f"{attr_name}={attr_value}")
            if attr_name != last_element:
                string.write(", ")
        string.write(")")
        return string.getvalue()

    def add_property(self, name, value):
        value = self.validate_property(name, value)
        self.__setattr__(name, value)

    def get_property(self, name):
        return self.__getattribute__(name)

    def validate_property(self, name, value):
        value = _replace_by_variables(value, self._variables_access.constants)
        annotation = self.__annotations__[name]
        if annotation == TIME:
            value = _manage_time(value, self._variables_access.metadata.frame_rate)
        else:
            value = annotation(value)
        return value
