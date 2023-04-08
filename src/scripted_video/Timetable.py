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
    object_name = ""
    if command[1][0] == "object_name":
        object_name = command[1][1]

    if not object_information.get(object_name, False):
        if classification != "C":
            raise UserWarning("Temporary exception for an object being called before it's created.")
        # This only occurs if the object doesn't already exist, likely to
        # happen if the object is trying to be created.
        object_information[object_name] = ImageObject(object_name)

    object_reference = object_information[object_name]  # object_reference
    # exists to prevent repetitive typing.

    for name, contents in command[2:]:
        object_reference.__setattr__(name, contents)

    if classification == "M":
        object_reference.check_move_alignment()

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
        self.start_time = None
        self.x = None
        self._x_current = None
        self.y = None
        self._y_current = None
        self.scale = None
        self._scale_current = None
        self.layer = None
        self.move_time = []
        self.move_x = []
        self.move_y = []
        self.move_scale = []
        self.move_rate = []
        self.delete_time = None
        self.delay = 0

    def __setattr__(self, name, value):
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