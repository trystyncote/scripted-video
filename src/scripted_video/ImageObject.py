from typing import Any


class ImageObject:
    def __init__(self, object_name: str):
        """
        Creates an object that is attached to an image. Only takes object_name
        initially, but requires most of the variables to properly work.

        :param object_name: Name of the object. Should be unique.
        """
        self._object_name = object_name
        self._file_name = None
        self.start_time = 0
        self.x = 0
        self._x_current = None
        self.y = 0
        self._y_current = None
        self.scale = 0.0
        self._scale_current = None
        self.layer = 0
        self.move_time: list[int] = []
        self.move_x: list[int] = []
        self.move_y: list[int] = []
        self.move_scale: list[float | int] = []
        self.move_rate: list[int] = []
        self.delete_time = 0
        self.delay = 0

    def __setattr__(self, name: str, value: Any):
        # if name not in self.__dict__:
        #     raise AttributeError(f"Attribute {name} not in ImageObject.")
        if name[0:4] == "move" and value != []:
            self.__dict__[name].append(value)
            return
        super().__setattr__(name, value)

    @property
    def object_name(self):
        """
        The name of the object, which is also the name of the instance, so to
        speak. Has no setter method, as this attribute shouldn't be changed.
        """
        return self._object_name

    @property
    def moves(self):
        return True if self.move_time else False

    def check_move_alignment(self):
        expected_length = len(self.move_time)

        # These if-statements are temporary, since the commands require these
        # parameters, so these if-statements are useless. This is a test part
        # of the code, since there are currently no optional parameters to the
        # MOVE OBJECT statement.
        if len(self.move_x) < expected_length:
            self.move_x.append(0)
        if len(self.move_y) < expected_length:
            self.move_y.append(0)
        if len(self.move_scale) < expected_length:
            self.move_scale.append(0.0)
        if len(self.move_rate) < expected_length:
            self.move_rate.append(1)

    def move_object(self, frame_index):
        move_index = 0
        # frame_difference = -1

        x_alter = 0
        y_alter = 0
        scale_alter = 0.0

        while True:
            try:
                if self.move_time[move_index] < frame_index \
                        < (self.move_time[move_index] + self.move_rate[move_index]):
                    # frame_difference = (frame_index - self._move_time[move_index])
                    x_alter += int(self.move_x[move_index] / self.move_rate[move_index])
                    y_alter += int(self.move_y[move_index] / self.move_rate[move_index])
                    scale_alter += (self.move_scale[move_index] / self.move_rate[move_index])
            except IndexError:
                break

            move_index += 1

        self.x += x_alter
        self.y += y_alter
        self.scale += scale_alter
