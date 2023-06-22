from src.scripted_video.objects._time import _manage_time, TIME

from src.scripted_video.variables.ScriptVariables import ScriptVariables

from pathlib import Path
import weakref
import io

from PIL import Image


def _property_slots():
    return ("layer", "move_rate", "move_scale", "move_time", "move_x", "move_y", "scale", "x", "y",
            "start_time", "delete_time", "delay")  # The latter three properties are eventually going to be defunct.


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
    move_rate: TIME
    move_scale: float
    move_time: TIME
    move_x: int
    move_y: int
    scale: float
    x: int
    y: int
    start_time: TIME
    delete_time: TIME
    delay: TIME

    def __init__(self):
        self._variables_access: ScriptVariables = None

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


def _loop_over_type(value, constants):
    for name in dir(constants):
        if name.startswith("__") or name.endswith("__"):
            continue
        value = value.replace(f"${name}", str(constants.get_variable(name)))
    return value


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


class ImageObject:
    __slots__ = ("_filename", "_finalizer", "_loaded_image", "_moves", "_object_name", "_loaded_pixels", "_properties",
                 "__weakref__")

    def __init__(self, object_name: str):
        self._filename = None
        self._finalizer = weakref.finalize(self, self.close)
        self._loaded_image = None
        self._loaded_pixels = None
        self._moves = False
        self._object_name = object_name
        self._properties = Properties()

    def __hash__(self):
        return hash(self._object_name)

    def __repr__(self):
        return f"{self.__class__.__name__}(object_name={self._object_name!r}, filename={self._filename!r}, " \
               f"properties={self._properties!r})"

    @property
    def is_opened(self):
        return True if self._loaded_image else False

    @property
    def moves(self):
        return self._moves

    @property
    def object_name(self):
        return self._object_name

    @property
    def properties(self):
        return self._properties

    def add_property(self, name, value):
        name = name.replace("-", "_")
        if name == "file_name":
            value = self._properties.validate_property(name, value)
            if self._filename is None:
                self._filename = Path(value) if isinstance(value, str) else value
                return
            else:
                raise KeyError(f"({self.__class__.__name__}) - Duplicate property name \'{name}\'.")
        elif name[0:4] == "move":
            self._moves = True
        elif hasattr(self._properties, name):
            raise KeyError(f"({self.__class__.__name__}) - Duplicate property name \'{name}\'.")
        self._properties.add_property(name, value)

    def close(self):
        if self._loaded_image is None:
            return
        self._loaded_image.close()
        self._loaded_image = None
        self._loaded_pixels = None

    def init_variables_instance(self, variables):
        if self._properties._variables_access is not None:
            return
        self._properties.init_variables_instance(variables)

    def get_image_height(self):
        if self._loaded_image is None:
            raise ReferenceError("Image File was not opened before call to get image height.")
        return self._loaded_image.height

    def get_image_width(self):
        if self._loaded_image is None:
            raise ReferenceError("Image File was not opened before call to get image width.")
        return self._loaded_image.width

    def get_pixel(self, x, y):
        if self._loaded_image is None:
            raise ReferenceError(f"Image File was not opened before call to get pixel at ({x}, {y}).")
        return self._loaded_pixels.__getitem__((x, y))

    def get_property(self, name):
        name = name.replace("-", "_")
        if name == "file_name":
            return self._filename
        return self._properties.get_property(name)

    def move_object(self, frame_index):
        move_index = -1
        alter_x = 0
        alter_y = 0
        alter_scale = 0.0

        while True:
            move_index += 1
            try:
                move_time = self._properties.move_time[move_index]
                move_rate = self._properties.move_rate[move_index]
                if move_time < frame_index < (move_time + move_rate):
                    alter_x += int(self._properties.move_x[move_index] / move_rate)
                    alter_y += int(self._properties.move_y[move_index] / move_rate)
                    alter_scale += float(self._properties.move_scale[move_index] / move_rate)
            except IndexError:
                break

        self._properties.x += alter_x
        self._properties.y += alter_y
        self._properties.scale += alter_scale

    def open(self):
        if self._filename is None:
            raise ReferenceError("Attribute 'file-name' not defined before call to open image.")
        self._loaded_image = Image.open(self._filename)
        if hasattr(self._properties, "scale"):
            width, height = self._loaded_image.size
            width = int(width * self._properties.scale + 0.99)
            height = int(height * self._properties.scale + 0.99)
            self._loaded_image = self._loaded_image.resize((width, height))
        self._loaded_pixels = self._loaded_image.load()
