from src.scripted_video.variables.ScriptVariables import ScriptVariables

from src.scripted_video.objects.ObjectDict import ObjectDict
from src.scripted_video.objects.ImageObject import ImageObject

from pathlib import Path
import re


def define_prefix(current_line: str, traits: ScriptVariables, object_information: ObjectDict):
    """
    Collects the information about the respective command from the
    'current_line' variable.

    :param current_line: The line with the command in it.
    :param traits: The video's traits, such as frame_rate.
    :param object_information: An ObjectDict that contains various object
        classes, such as ImageObject.
    :return: Returns the necessary information from the command without the
        extraneous content.
    """
    if re.match(r"HEAD ((f((rame_rate)|(ile_name)))|(window_((width)|(height))))(\s|)=(\s|)[\w_]*", current_line):
        _command_head(current_line, traits)

    elif re.match(r"SET [\w_]*(\s|)=(\s|)[\w.'\"\\]* AS \w*", current_line):
        _command_set(current_line, traits)

    elif re.match(r"CREATE OBJECT [\w_]*: [\w_]*", current_line):
        _command_object_create(current_line, traits, object_information)

    elif re.match(r"MOVE OBJECT [\w_]*: [\w_]*", current_line):
        _command_object_move(current_line, traits, object_information)

    elif re.match(r"DELETE OBJECT [\w_]*: [\w_]*", current_line):
        _command_object_delete(current_line, traits, object_information)

    else:
        raise UserWarning(f"Temporary exception for an unrecognized command, {current_line!r}")


def _command_head(command: str, traits: ScriptVariables):
    HEAD_ = command.find("HEAD ") + 5
    equal_sign = command.find("=")

    keyword = command[HEAD_:equal_sign].strip()
    contents: (int | str) = command[equal_sign+1:].strip()

    if keyword == "window_width" or keyword == "window_height" or keyword == "frame_rate":
        contents = int(contents)
    elif keyword == "file_name":
        pass
    else:
        raise ValueError

    traits.metadata.update_value(keyword, contents)
    # return traits


def _command_set(command: str, traits: ScriptVariables):
    SET_ = command.find("SET ") + 4
    equal_sign = command.find("=")
    _AS_ = command.find(" AS ")

    name = command[SET_:equal_sign].strip()
    value: (bool | float | int | Path | str) = command[(equal_sign+1):_AS_].strip()
    type_ = command[(_AS_+4):].strip().upper()

    if type_ == "ADDRESS":
        if value == "__current_address__":
            value = traits.metadata.script_file.parent
        else:
            value = Path(str(value))

    elif type_ == "BOOL":
        assert isinstance(value, str)  # This 'assert' keyword is here to
        # prevent mypy from raising a [union-attr] error.
        if value.upper() == "TRUE":
            value = True
        elif value.upper() == "FALSE":
            value = False
        else:
            raise ValueError

    elif type_ == "FLOAT":
        value = float(str(value))

    elif type_ == "INT":
        value = int(str(value))

    elif type_ == "STRING":
        pass  # This section does nothing but allow the script to not evaluate
        # the 'else' clause, which is for raising an error for when `type_` is
        # invalid.

    else:
        raise ValueError

    traits.constants.call_relevant(type_).create_variable(name, value)
    # return traits


def _command_object_create(command: str, traits: ScriptVariables, object_information: ObjectDict):
    CREATE_OBJECT_ = command.find("CREATE OBJECT ") + 14
    colon = command.find(":")

    object_name = command[CREATE_OBJECT_:colon].strip()
    keys = _split_by_keys(command[(colon + 1):], 6)

    relevant_object = ImageObject(object_name)
    relevant_object.init_variables_instance(traits)

    relevant_object.add_property("file-name", keys[0])
    relevant_object.add_property("start-time", keys[1])
    relevant_object.add_property("x", keys[2])
    relevant_object.add_property("y", keys[3])
    relevant_object.add_property("scale", keys[4])
    relevant_object.add_property("layer", keys[5])

    if len(keys) > 6:
        extra_keys = _split_extra_keys(keys[6:])

        for key, value in extra_keys:
            relevant_object.add_property(key, value)

    object_information[relevant_object.object_name] = relevant_object
    # return object_information


def _command_object_move(command: str, traits: ScriptVariables, object_information: ObjectDict):
    MOVE_OBJECT_ = command.find("MOVE OBJECT ") + 12
    colon = command.find(":")

    object_name = command[MOVE_OBJECT_:colon].strip()
    keys = _split_by_keys(command[(colon + 1):], 5)

    relevant_object = object_information[object_name]

    relevant_object.add_property("move-time", keys[0])
    relevant_object.add_property("move-x", keys[1])
    relevant_object.add_property("move-y", keys[2])
    relevant_object.add_property("move-scale", keys[3])
    relevant_object.add_property("move-rate", keys[4])

    if len(keys) > 5:
        extra_keys = _split_extra_keys(keys[5:])

        for key, value in extra_keys:
            relevant_object.add_property(f"{'move-' if key[0:4] != 'move' else ''}{key}", value)

    relevant_object.check_move_alignment()
    # return object_information


def _command_object_delete(command: str, traits: ScriptVariables, object_information: ObjectDict):
    DELETE_OBJECT_ = command.find("DELETE OBJECT ") + 14
    colon = command.find(":")

    object_name = command[DELETE_OBJECT_:colon].strip()
    keys = _split_by_keys(command[(colon + 1):], 1)

    relevant_object = object_information[object_name]

    relevant_object.add_property("delete-time", keys[0])

    if len(keys) > 1:
        extra_keys = _split_extra_keys(keys[1:])

        for key, value in extra_keys:
            relevant_object.add_property(key, value)

    # return object_information


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


def _split_by_keys(string_keys: str, minimum: int):
    keys = string_keys.split(",")
    keys = [k.strip() for k in keys]
    if len(keys) < minimum:
        raise UserWarning("Temporary exception for having too few keys.")
    return keys


def _split_extra_keys(keys_series):
    keys = []
    for item in keys_series:
        keys.append(item.split("=", 1))
        if len(keys[-1]) != 2:
            raise UserWarning("Temporary exception for excess keys or multiple equal signs.")
        keys[-1][0] = keys[-1][0].lower()
    return keys
