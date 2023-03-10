from Timetable import ImageObject

import re


def define_prefix(current_line: str, traits: dict):
    """
    Collects the information about the respective command from the
    'current_line' variable.

    :param current_line: The line with the command in it.
    :param traits: The video's traits, such as frame_rate.
    :return: Returns the necessary information from the command without the
        extraneous content.
    """
    split_current_line = current_line.split(" ")  # split_current_line houses
    # the tuple with the information separated by whitespace. This is for
    # readability purposes.

    if split_current_line[0].upper() == "HEAD":
        return _command_head(current_line, **traits), 1

    elif split_current_line[0] == "SET":
        return _command_set(current_line, **traits), 1

    elif split_current_line[0] == "CREATE" and split_current_line[1] == "OBJECT":
        return _command_object_create(current_line, **traits), 2

    elif split_current_line[0] == "MOVE" and split_current_line[1] == "OBJECT":
        return _command_object_move(current_line, **traits), 2

    elif split_current_line[0] == "DELETE" and split_current_line[1] == "OBJECT":
        return _command_object_delete(current_line, **traits), 2

    raise UserWarning("Temporary exception for an unrecognized command.")


def _manage_time(time_string: str, frame_rate: int):
    time_string = (time_string + " ").split(" ")  # time_string splits itself
    # by the whitespace because the full command must be split that way by
    # default. Example: "2s 15f" refers to 2 seconds, and 15 frames after that.
    _ = time_string.pop(-1)
    # f: frame, s: seconds, m: minutes, h: hours
    suffix_effect = {"f": 1,
                     "s": frame_rate,  # The amount of frames per second is a
                     "m": frame_rate*60,  # variable amount, so it's manually
                     "h": frame_rate*60*60}  # calculated here.

    time = 0.0  # This variable is to store the amount of frames per unit as
    # it is iterated over.
    for i in time_string:
        time += float(i[:-1]) * suffix_effect[i[-1]]  # The float member of the
        # number 'i[:-1]', meaning before the suffix, is multiplied by the
        # suffix effect denoted by the specific character.

    return int(time)


def _collect_syntax_snapshot(full_line, re_match_instance: re.Match, re_match_instance_additional: re.Match = None):
    if re_match_instance_additional is None:
        return full_line[re_match_instance.start():re_match_instance.end()]
    return full_line[re_match_instance.end():re_match_instance_additional.start()]


def _command_head(current_line: str, **traits):
    syntax_full = "HEAD ((f((rame_rate)|(ile_name)))|(window_((width)|(height))))(\s|)=(\s|)[0-9A-Za-z_]*"
    # HEAD window_width = 852
    # ^^^^^^^^^^^^^^^^^^^^^^^
    if not re.match(syntax_full, current_line):
        # %&$ Raise exception for the script.
        pass

    syntax_keyword = "f((rame_rate)|(ile_name))|(window_((width)|(height)))"
    # HEAD window_width = 852
    #      ^^^^^^^^^^^^
    keyword = re.search(syntax_keyword, current_line)
    keyword = _collect_syntax_snapshot(current_line, keyword).strip()

    syntax_equal_sign = "="
    # HEAD window_width = 852
    #                   ^
    equal_sign = re.search(syntax_equal_sign, current_line)

    syntax_contents = "[\w\s-]*"
    # (Only to be used for the part of the string after the equal sign.)
    # HEAD window_width = 852
    #                     ^^^
    contents = re.search(syntax_contents, current_line[equal_sign.end():])
    contents = _collect_syntax_snapshot(current_line[equal_sign.end():], contents).strip()

    if keyword == "window_width" or keyword == "window_height" or keyword == "frame_rate":
        contents = int(contents)

    traits["_HEAD"][keyword] = contents
    return traits


def _command_set(current_line: str, **traits):
    syntax_full = "SET [0-9A-Za-z_]*(\s|)=(\s|)[0-9A-Za-z_]* AS [0-9A-Za-z_]*"
    # SET variable = value AS type
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    if not re.match(syntax_full, current_line):
        # %&$ Raise exception for the script.
        pass

    syntax_SET_ = "SET "
    # SET variable = value AS type
    # ^^^
    SET_ = re.search(syntax_SET_, current_line)

    syntax_equal_sign = "="
    # SET variable = value AS type
    #              ^
    equal_sign = re.search(syntax_equal_sign, current_line)

    classify_variable = current_line[SET_.end():equal_sign.start()].strip()
    syntax__AS_ = " AS "
    # SET variable = value AS type
    #                      ^^
    _AS_ = re.search(syntax__AS_, current_line)

    classify_value = current_line[equal_sign.end():_AS_.start()].strip()
    classify_type = current_line[_AS_.end():].strip()

    if classify_type.upper() == "INT":
        classify_value = int(classify_value)

    elif classify_type.upper() == "FLOAT":
        classify_value = float(classify_value)

    elif classify_type.upper() == "BOOL":
        classify_value = bool(classify_value)

    elif classify_type.upper() == "STRING":
        pass

    elif classify_type.upper() == "ADDRESS":
        if classify_value == "__current_address__":
            classify_value = traits["_HEAD"]["_script_name"]
            classify_value = classify_value.rsplit("\\", 1)
            classify_value = classify_value[0] + "\\"

    else:
        # %&$ Raise exception for the script.
        pass

    traits[classify_type][classify_variable] = classify_value
    return traits


def _command_object_create(current_line: str, **traits):
    syntax_full = "CREATE OBJECT \w*: \w*"
    # CREATE OBJECT objectname: filename, start_time, ...
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^~~~~~~~~~~~~~ ...
    if not re.match(syntax_full, current_line):
        # %&$ Raise exception for the script.
        pass

    syntax_CREATE_OBJECT_ = "CREATE OBJECT "
    # CREATE OBJECT objectname: filename, start_time, ...
    # ^^^^^^^^^^^^^
    CREATE_OBJECT_ = re.search(syntax_CREATE_OBJECT_, current_line)

    syntax_colon = ":"
    # CREATE OBJECT objectname: filename, start_time, ...
    #                         ^
    colon = re.search(syntax_colon, current_line)

    object_name = _collect_syntax_snapshot(current_line, CREATE_OBJECT_, colon)
    # object_name = current_line[CREATE_OBJECT_.end():colon.start()]

    keys = _split_by_keys(current_line[colon.end():], 6)

    keys_contained = [
        "C",
        ("object_name", object_name),
        ("file_name", keys[0]),
        ("start_time", keys[1]),
        ("x", keys[2]),
        ("y", keys[3]),
        ("scale", keys[4]),
        ("layer", keys[5])
    ]

    if len(keys) > 6:
        keys_contained = _split_extra_keys(keys_contained, keys[6:])

    return keys_contained


def _command_object_move(current_line: str, **traits):
    syntax_full = "MOVE OBJECT \w*: \w*"
    # MOVE OBJECT objectname: change_time, x_change, ...
    # ^^^^^^^^^^^^^^^^^^^^^^^~~~~~~~~~~~~~~~~~~~~~~~ ...
    if not re.match(syntax_full, current_line):
        # %&$ Raise exception for the script.
        pass

    syntax_MOVE_OBJECT_ = "MOVE OBJECT "
    # MOVE OBJECT objectname: move_time, x, y, ...
    # ^^^^^^^^^^^
    MOVE_OBJECT_ = re.search(syntax_MOVE_OBJECT_, current_line)

    syntax_colon = ":"
    # MOVE OBJECT objectname: move_time, x, y, ...
    #                       ^
    colon = re.search(syntax_colon, current_line)

    object_name = _collect_syntax_snapshot(current_line, MOVE_OBJECT_, colon)
    # object_name = current_line[MOVE_OBJECT_.end():colon.start()]

    keys = _split_by_keys(current_line[colon.end():], 5)

    keys_contained = [
        "M",
        ("object_name", object_name),
        ("move_time", keys[0]),
        ("move_x", keys[1]),
        ("move_y", keys[2]),
        ("move_scale", keys[3]),
        ("move_rate", keys[4])
    ]

    if len(keys) > 5:
        keys_contained = _split_extra_keys(keys_contained, keys[5:])

    return keys_contained


def _command_object_delete(current_line: str, **traits):
    syntax_full = "DELETE OBJECT \w*: \w*"
    # DELETE OBJECT objectname: delete_time, ...
    # ^^^^^^^^^^^^^^^^^^^^^^^^^~~~~~~~~~~~~~ ...
    if not re.match(syntax_full, current_line):
        # %&$ Raise exception for the script.
        pass

    syntax_DELETE_OBJECT_ = "DELETE OBJECT "
    # DELETE OBJECT objectname: filename, start_time, ...
    # ^^^^^^^^^^^^^
    DELETE_OBJECT_ = re.search(syntax_DELETE_OBJECT_, current_line)

    syntax_colon = ":"
    # DELETE OBJECT objectname: filename, start_time, ...
    #                         ^
    colon = re.search(syntax_colon, current_line)

    object_name = _collect_syntax_snapshot(current_line, DELETE_OBJECT_, colon)
    # object_name = current_line[DELETE_OBJECT_.end():colon.start()]

    keys = _split_by_keys(current_line[colon.end():], 1)

    keys_contained = [
        "D",
        ("object_name", object_name),
        ("delete_time", keys[0])
    ]

    if len(keys) > 1:
        keys_contained = _split_extra_keys(keys_contained, keys[1:])

    return keys_contained


def _split_by_keys(string_keys: str, minimum: int):
    keys = string_keys.split(",")
    keys = [k.strip() for k in keys]
    if len(keys) < minimum:
        raise UserWarning("Temporary exception for having too few keys.")
    return keys


def _split_extra_keys(keys_contained: list, keys_series: list):
    for keys_item in keys_series:
        keys_contained.append(keys_item.split("=", 1))
        if len(keys_contained[-1]) != 2:
            raise UserWarning("Temporary exception for excess keys or multiple equal signs.")
        keys_contained[-1][0] = keys_contained[-1][0].lower()
        keys_contained[-1] = tuple(keys_contained[-1])
    return keys_contained
