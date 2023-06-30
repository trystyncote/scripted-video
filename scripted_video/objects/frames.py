from scripted_video.objects.ObjectDict import ObjectDict

from PIL import Image


class Frame:
    def __init__(self, index: int, size: tuple[int, int]):
        self._frame = None
        self.index = index
        self.object: list[str] = []
        self._size = size

    def __repr__(self):
        return f"{self.__class__.__name__}(index={self.index}, object={self.object})"

    def add_object(self, name: str):
        if name in self.object:
            return
        self.object.append(name)

    def clear_frame(self):
        self._frame = None

    def draw_frame(self, object_dictionary: ObjectDict, filename_prefix: str):
        if self._frame:
            self.index += 1
            self.save_frame(filename_prefix)
            return

        object_set = set(object_dictionary[obj] for obj in self.object)
        frame = Image.new("RGB", self._size, (255, 255, 255))
        self._frame = frame
        frame_pixel = frame.load()

        for obj in object_set:
            obj_x = obj.get_property("x")
            obj_y = obj.get_property("y")

            for x in range(obj_x, obj_x + obj.get_image_width()):
                for y in range(obj_y, obj_y + obj.get_image_height()):
                    try:
                        frame_pixel.__setitem__((x, y), obj.get_pixel(x - obj_x, y - obj_y))
                    except IndexError:
                        pass

        self.save_frame(filename_prefix)

    def save_frame(self, filename_prefix: str):
        self._frame.save(f"{filename_prefix}\\{self.index}.png", "PNG")
