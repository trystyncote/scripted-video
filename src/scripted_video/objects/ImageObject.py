from src.scripted_video.objects.instruction import RootInstruction
from src.scripted_video.objects.properties import Properties

from pathlib import Path
import weakref

from PIL import Image


class ImageObject:
    __slots__ = ("_adjustments", "_filename", "_finalizer", "_loaded_image", "_object_name", "_loaded_pixels",
                 "_properties", "__weakref__")

    _adjustments: list[RootInstruction]

    def __init__(self, object_name: str):
        self._adjustments = []
        self._filename = None
        self._finalizer = weakref.finalize(self, self.close)
        self._loaded_image = None
        self._loaded_pixels = None
        self._object_name = object_name
        self._properties = Properties()

    def __hash__(self):
        return hash(self._object_name)

    def __repr__(self):
        return f"{self.__class__.__name__}(filename={self._filename!r}, object_name={self._object_name!r}, " \
               f"properties={self._properties!r} )"

    @property
    def adjustments(self):
        return self._adjustments

    @property
    def is_opened(self):
        return True if self._loaded_image else False

    @property
    def moves(self):
        return bool(self._adjustments)

    @property
    def object_name(self):
        return self._object_name

    @property
    def properties(self):
        return self._properties

    def add_adjustment(self, adjustment):
        if adjustment.bound_object != self._object_name:
            raise AttributeError(f"Bound object of \'{adjustment.__class__}\' ({adjustment.bound_object}) doesn't match"
                                 f" object name of \'{self.__class__}\' ({self._object_name})")
        self._adjustments.append(adjustment)

    def add_property(self, name, value):
        name = name.replace("-", "_")
        if name == "file_name":
            value = self._properties.validate_property(name, value)
            if self._filename is None:
                self._filename = Path(value) if isinstance(value, str) else value
                return
            else:
                raise KeyError(f"({self.__class__.__name__}) - Duplicate property name \'{name}\'.")
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
        for instruction in self._adjustments:
            alter_x, alter_y, alter_scale = instruction.carry_out_instruction(frame_index)
            # This representation of .carry_out_instruction() is not fully
            # set in stone. This needs to be renovated if multiple types of
            # instructions are going to be added.
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
