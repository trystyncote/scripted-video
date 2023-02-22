# NOTE TO SELF: 2023-02-07  00:05
#   Possible solution to custom exceptions is a class that contains each
#   exception and prints it as an ExceptionGroup. "ExceptionCollection"?

def create_timetable(timetable_information: list, variable_data: dict = None):
    """
    Creates a timetable for the video.

    :param timetable_information: The information about the objects as per the
        OBJECT keyword.
    :param variable_data: The data about any variables that are created by the
        SET keyword.
    :return sorted_timetable: The full timetable, with is a 2-d list with
        the names of the object that is on that frame (x-axis), on that layer.
        (y-axis)
    :return object_information: The contents of each object by its name. Each
        name refers to an instance of the ImageObject class, which stores each
        trait of the object, such as x-coordinate or scale.
    """
    if variable_data is None:
        # Mutable default.
        variable_data = {}

    object_information = {}  # object_information will hold a reference to each
    # instance of a class with the information about an object to be drawn on
    # screen.

    for command in timetable_information:
        # Each command in timetable_information is a list that looks similar to
        # ["x", info, info, ...], with is then dissected into an instance of
        # the ImageObject class. Position of what goes where is hard-coded!
        object_information = _collect_information(command, object_information,
                                                  variable_data)

    sorted_timetable = _define_dimensions(object_information)
    # sorted_timetable is a 2-d list that stores the name of an object in a
    # member of itself. The x-axis is for frames of the video, and the y-axis
    # is for the layer it is on. Lower layer number is further back.
    sorted_timetable = _fill_timetable(sorted_timetable, object_information)
    # The timetable is filled second, to prevent any out-of-order errors.
    # The first test script (scriptedvideo_sample_script_1.txt) doesn't have
    # this issue.

    return sorted_timetable, object_information


def _collect_information(command: list, object_information: dict,
                         variable_data: dict):
    classification = command[0]  # "C" (Create), "M" (Move), or "D" (Delete).
    object_name = command[1]

    if not object_information.get(object_name, False):
        # This only occurs if the object doesn't already exist, likely to
        # happen if the object is trying to be created.
        object_information[object_name] = ImageObject(object_name)

    object_reference = object_information[object_name]  # object_reference
    # exists to prevent repetitive typing.

    # "C", objectname, filename, time, x, y, scale, layer
    if classification == "C":
        object_reference.file_name = command[2]
        for key in variable_data:
            # This loop checks to see if there are any variables in the
            # file_name variable. If there are, replace it with the variable's
            # contents.
            if object_reference.file_name.find(key) != -1:
                object_reference.file_name = object_reference.file_name \
                    .replace(key + "/", variable_data[key])

        # Positions are all hard-coded!
        object_reference.add_create_details(start_time=command[3], x=command[4], y=command[5], scale=command[6],
                                            layer=command[7])

    # "M", objectname, time, x', y', scale', rate
    elif classification == "M":
        # Positions are all hard-coded!
        object_reference.add_move_details(move_time=command[2], x_change=command[3], y_change=command[4],
                                          scale_change=command[5], move_rate=command[6])

    # "D", objectname, time, delay
    elif classification == "D":
        # Positions are all hard-coded!
        object_reference.add_delete_details(delete_time=command[2], delete_delay=command[3])

    return object_information


def _define_dimensions(object_information: dict):
    sorted_timetable = []
    find_max_frame = []  # find_max_frame and find_max_layer store each
    find_max_layer = []  # occurrence of either number.

    for key in object_information:
        find_max_frame.append(object_information[key].start_time)
        find_max_frame.append(object_information[key].delete_time)
        find_max_layer.append(object_information[key].layer)

    max_frame = max(find_max_frame)
    max_layer = max(find_max_layer) + 1  # max_layer adds one extra to allow
    # index 0 to store audio. Currently, that's non-functional.

    for frame_num in range(max_frame):
        sorted_timetable.append([])
        for layer_num in range(max_layer):
            sorted_timetable[frame_num].append("")

    return sorted_timetable


def _fill_timetable(sorted_timetable: list, object_information: dict):
    for key in object_information:
        object_reference = object_information[key]
        start = object_reference.start_time
        end = object_reference.delete_time

        for frame_index in range(end - start):
            sorted_timetable[start+frame_index][object_reference.layer] = key

    return sorted_timetable


class ImageObject:
    def __init__(self, object_name: str):
        """
        Creates an object that is attached to an image. Only takes object_name
        initially, but requires most of the variables to properly work.

        :param object_name: Name of the object. Should be unique.
        """
        self._object_name = object_name
        self._file_name = None
        self._start_time = None
        self._x_coord = None
        self._x_current = None
        self._y_coord = None
        self._y_current = None
        self._scale = None
        self._scale_current = None
        self._layer = None
        self._move = False
        self._move_index = 0
        self._move_time = []
        self._move_x = []
        self._move_y = []
        self._move_scale = []
        self._move_rate = []
        self._delete_time = None
        self._delete_delay = None

    def __iter__(self):
        return self

    def __next__(self):
        if not self._move:
            self._move_index = -1
            raise StopIteration

        self._move_index += 1
        try:
            return self._move_time[self._move_index], self._move_x[self._move_index], self._move_y[self._move_index], \
                self._move_scale[self._move_index], self._move_rate[self._move_index]
        except IndexError:
            self._move_index = -1
            raise StopIteration

    @property
    def object_name(self):
        """
        The name of the object, which is also the name of the instance, so to
        speak. Has no setter method, as this attribute shouldn't be changed.
        """
        return self._object_name

    @property
    def file_name(self):
        """
        The name of the file that the object is portrayed as. Should be a .png,
        .jpg, or .bmp file.
        """
        return self._file_name

    @file_name.setter
    def file_name(self, file_name: str):
        self._file_name = file_name

    @property
    def start_time(self):
        """
        The time that the object first appears in the video. The measurement is
        in frames.
        """
        return self._start_time

    @property
    def x(self):
        """
        The x-coordinate of the image. The position in question is for the
        top-left corner of the image. Measured in pixels from the top-left-most
        corner.
        """
        return self._x_current

    @property
    def y(self):
        """
        The y-coordinate of the image. The position in question is for the
        top-left corner of the image. Measured in pixels from the top-left-most
        corner.
        """
        return self._y_current

    @property
    def scale(self):
        """
        The scale of the image. The measurement is a decimal point, where 1.0
        is 100%, 0.9 is 90%, etc.
        """
        return self._scale_current

    @property
    def layer(self):
        """
        The layer that the image should be placed on. Lower numbers are farther
        back on the image.
        """
        return self._layer

    @property
    def moves(self):
        return self._move

    @property
    def delete_time(self):
        """
        The time that the object is removed from the video. The measurement is
        in frames.
        """
        return self._delete_time

    @property
    def delete_delay(self):
        """
        The rate that the object is delayed from being removed. A delay of '0'
        means it is deleted immediately. The measurement is in frames.
        """
        return self._delete_delay

    def add_create_details(self, *, start_time: int, x: int, y: int, scale: float, layer: int):
        self._start_time = start_time
        self._x_coord = x
        self._x_current = x
        self._y_coord = y
        self._y_current = y
        self._scale = scale
        self._scale_current = scale
        self._layer = layer

    def add_move_details(self, *, move_time: int, x_change: int, y_change: int,
                         scale_change: float, move_rate: int):
        self._move = True
        self._move_time.append(move_time)
        self._move_x.append(x_change)
        self._move_y.append(y_change)
        self._move_scale.append(scale_change)
        self._move_rate.append(move_rate)

    def add_delete_details(self, *, delete_time: int, delete_delay: int):
        self._delete_time = delete_time
        self._delete_delay = delete_delay

    def move_object(self, frame_index):
        move_index = 0
        # frame_difference = -1

        x_alter = 0
        y_alter = 0
        scale_alter = 0.0

        while True:
            try:
                if self._move_time[move_index] < frame_index \
                        < (self._move_time[move_index] + self._move_rate[move_index]):
                    # frame_difference = (frame_index - self._move_time[move_index])
                    x_alter += int(self._move_x[move_index] / self._move_rate[move_index])
                    y_alter += int(self._move_y[move_index] / self._move_rate[move_index])
                    scale_alter += (self._move_scale[move_index] / self._move_rate[move_index])
            except IndexError:
                break

            move_index += 1

        self._x_current += x_alter
        self._y_current += y_alter
        self._scale_current += scale_alter
