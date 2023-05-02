# NOTE TO SELF: 2023-02-07  00:05
#   Possible solution to custom exceptions is a class that contains each
#   exception and prints it as an ExceptionGroup. "ExceptionCollection"?
from src.scripted_video.ImageObject import ImageObject


def create_timetable(timetable_information: list[str | list[str]]):
    """
    Creates a timetable for the video.

    :param timetable_information: The information about the objects as per the
        OBJECT keyword.
    :return sorted_timetable: The full timetable, with is a 2-d list with
        the names of the object that is on that frame (x-axis), on that layer.
        (y-axis)
    :return object_information: The contents of each object by its name. Each
        name refers to an instance of the ImageObject class, which stores each
        trait of the object, such as x-coordinate or scale.
    """

    object_information = {}  # object_information will hold a reference to each
    # instance of a class with the information about an object to be drawn on
    # screen.

    for command in timetable_information:
        # Each command in timetable_information is a list that looks similar to
        # ["x", info, info, ...], with is then dissected into an instance of
        # the ImageObject class. Position of what goes where is hard-coded!
        object_information = _collect_information(command, object_information)

    sorted_timetable = _define_dimensions(object_information)
    # sorted_timetable is a 2-d list that stores the name of an object in a
    # member of itself. The x-axis is for frames of the video, and the y-axis
    # is for the layer it is on. Lower layer number is further back.
    sorted_timetable = _fill_timetable(sorted_timetable, object_information)
    # The timetable is filled second, to prevent any out-of-order errors.
    # The first test script (scriptedVideo_demoScript_1.txt) doesn't have
    # this issue.

    return sorted_timetable, object_information


def _collect_information(command: (str | list[str]), object_information: dict[str, ImageObject]):
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
