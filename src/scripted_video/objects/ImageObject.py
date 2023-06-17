from src.scripted_video.variables.ScriptVariables import ScriptVariables

from pathlib import Path
import weakref
import io

from PIL import Image


class PropertySlots:
    __slots__ = ("layer", "move_rate", "move_scale", "move_time", "move_x", "move_y", "scale", "x", "y",
                 "start_time", "delete_time", "delay")  # The latter three
    # properties are eventually going to be defunct.


class Originals(PropertySlots):
    def get_property(self, name):
        return self.__getattribute__(name)

    def set_property(self, name, value):
        self.__setattr__(name, value)


class Properties(PropertySlots):
    __slots__ = ("_original", "_variables_access")

    type_classifications = {
        "file_name": str,
        "layer": int,
        "move_rate": "TIME",
        "move_scale": float,
        "move_time": "TIME",
        "move_x": int,
        "move_y": int,
        "scale": float,
        "x": int,
        "y": int,
        "start_time": "TIME",
        "delete_time": "TIME",
        "delay": "TIME"
    }

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
        property_type = self.type_classifications[name]
        if property_type == "TIME":
            value = _manage_time(value, self._variables_access.metadata.frame_rate)
        else:
            value = property_type(value)
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


def _manage_time(time_string: str, frame_rate: int):
    time_string_list = (time_string + " ").split(" ")  # time_string splits itself
    # by the whitespace because the full command must be split that way by
    # default. Example: "2s 15f" refers to 2 seconds, and 15 frames after that.
    _ = time_string_list.pop(-1)
    # f: frame, s: seconds, m: minutes, h: hours
    suffix_effect = {"f": 1,
                     "s": frame_rate,  # The amount of frames per second is a
                     "m": frame_rate * 60,  # variable amount, so it's manually
                     "h": frame_rate * 60 * 60}  # calculated here.

    time = 0.0  # This variable is to store the amount of frames per unit as
    # it is iterated over.
    for i in time_string_list:
        time += float(i[:-1]) * suffix_effect[i[-1]]  # The float member of the
        # number 'i[:-1]', meaning before the suffix, is multiplied by the
        # suffix effect denoted by the specific character.

    return int(time)


class ImageObject:
    __slots__ = ("_filename", "_finalizer", "_loaded_image", "_moves", "_new_properties", "_object_name",
                 "_loaded_pixels", "_properties", "__weakref__")

    def __init__(self, object_name: str):
        self._filename = None
        self._finalizer = weakref.finalize(self, self.close)
        self._loaded_image = None
        self._loaded_pixels = None
        self._moves = False
        self._new_properties = []
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
            value = Properties.validate_property(self._properties, "file_name", value)
            if self._filename is None:
                self._filename = Path(value) if isinstance(value, str) else value
                return
            else:
                raise KeyError(f"({self.__class__.__name__}) - Duplicate property name \'{name}\'.")
        elif name[0:4] == "move":
            self._moves = True
        elif hasattr(self._properties, name):
            raise KeyError(f"({self.__class__.__name__}) - Duplicate property name \'{name}\'.")
        self._new_properties.append(name)
        self._properties.add_property(name, value)

    def check_move_alignment(self):
        expected_length = len(self._properties.move_time)

        # These if-statements are temporary, since the commands require these
        # parameters, so these if-statements are useless. This is a test part
        # of the code, since there are currently no optional parameters to the
        # MOVE OBJECT statement.
        while True:
            full_loop = True
            if len(self._properties.move_x) < expected_length:
                self._properties.move_x.append(0)
                full_loop = False
            if len(self._properties.move_y) < expected_length:
                self._properties.move_y.append(0)
                full_loop = False
            if len(self._properties.move_scale) < expected_length:
                self._properties.move_scale.append(0.0)
                full_loop = False
            if len(self._properties.move_rate) < expected_length:
                self._properties.move_rate.append(1)
                full_loop = False

            if full_loop:
                break

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
