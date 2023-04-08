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


def _collect_syntax_snapshot(full_line, re_match_instance: re.Match, re_match_instance_additional: re.Match = None):
    if re_match_instance_additional is None:
        return full_line[re_match_instance.start():re_match_instance.end()]
    return full_line[re_match_instance.end():re_match_instance_additional.start()]


def _command_head(current_line: str, **traits):
    syntax_full = r"HEAD ((f((rame_rate)|(ile_name)))|(window_((width)|(height))))(\s|)=(\s|)[\w_]*"
    # HEAD window_width = 852
    # ^^^^^^^^^^^^^^^^^^^^^^^
    if not re.match(syntax_full, current_line):
        # %&$ Raise exception for the script.
        raise UserWarning("SyntaxIssue: HEAD keyword")

    syntax_keyword = r"f((rame_rate)|(ile_name))|(window_((width)|(height)))"
    # HEAD window_width = 852
    #      ^^^^^^^^^^^^
    keyword = re.search(syntax_keyword, current_line)
    keyword = _collect_syntax_snapshot(current_line, keyword).strip()

    syntax_equal_sign = r"="
    # HEAD window_width = 852
    #                   ^
    equal_sign = re.search(syntax_equal_sign, current_line)

    syntax_contents = r"[[\w]\s-]*"
    # (Only to be used for the part of the string after the equal sign.)
    # HEAD window_width = 852
    #                     ^^^
    contents = re.search(syntax_contents, current_line[equal_sign.end():])
    contents = _collect_syntax_snapshot(current_line[equal_sign.end():], contents).strip()
    if contents.strip() == "":
        raise ValueError

    if keyword == "window_width" or keyword == "window_height" or keyword == "frame_rate":
        contents = int(contents)

    traits["_HEAD"][keyword] = contents
    return traits


def _command_set(current_line: str, **traits):
    syntax_full = r"SET [\w_]*(\s|)=(\s|)[\w.'\"\\]* AS [\w]*"
    # SET variable = value AS type
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    if not re.match(syntax_full, current_line):
        # %&$ Raise exception for the script.
        raise UserWarning("SyntaxIssue: SET keyword")

    syntax_SET_ = r"SET "
    # SET variable = value AS type
    # ^^^
    SET_ = re.search(syntax_SET_, current_line)

    syntax_equal_sign = r"="
    # SET variable = value AS type
    #              ^
    equal_sign = re.search(syntax_equal_sign, current_line)

    classify_variable = current_line[SET_.end():equal_sign.start()].strip()
    syntax__AS_ = r" AS "
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
        if classify_value.upper() == "TRUE":
            classify_value = True
        elif classify_value.upper() == "FALSE":
            classify_value = False
        else:
            raise ValueError(f"Expected True or False, got {classify_value}")

    elif classify_type.upper() == "STRING":
        pass

    elif classify_type.upper() == "ADDRESS":
        if classify_value == "__current_address__":
            classify_value = traits["_HEAD"]["_script_name"]
            classify_value = classify_value.rsplit("\\", 1)
            classify_value = classify_value[0] + "\\"

    else:
        # %&$ Raise exception for the script.
        raise UserWarning("Variable 'classify_value' not valid.")

    traits[classify_type][classify_variable] = classify_value
    return traits


def _command_object_create(current_line: str, **traits):
    syntax_full = r"CREATE OBJECT [\w_]*: [\w_]*"
    # CREATE OBJECT objectname: filename, start_time, ...
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^~~~~~~~~~~~~~ ...
    if not re.match(syntax_full, current_line):
        # %&$ Raise exception for the script.
        raise UserWarning("SyntaxIssue: CREATE OBJECT keyword")

    CREATE_OBJECT_ = re.search("CREATE OBJECT ", current_line)
    # CREATE OBJECT objectname: filename, start_time, ...
    # ^^^^^^^^^^^^^
    if CREATE_OBJECT_ is None:
        raise UserWarning("SyntaxIssue: CREATE OBJECT keyword; \'CREATE_OBJECT_\'.")

    colon = re.search(":", current_line)
    # CREATE OBJECT objectname: filename, start_time, ...
    #                         ^
    if colon is None:
        raise UserWarning("SyntaxIssue: CREATE OBJECT keyword; \'colon\'.")

    object_name = _collect_syntax_snapshot(current_line, CREATE_OBJECT_, colon)
    # object_name = current_line[CREATE_OBJECT_.end():colon.start()]

    keys = _split_by_keys(current_line[colon.end():], 6)

    keys_contained = [
        "C",
        ["object_name", object_name],
        ["file_name", keys[0]],
        ["start_time", keys[1]],
        ["x", keys[2]],
        ["y", keys[3]],
        ["scale", keys[4]],
        ["layer", keys[5]]
    ]

    if len(keys) > 6:
        keys_contained = _split_extra_keys(keys_contained, keys[6:])

    keys_contained = _evaluate_values(keys_contained, **traits)

    return keys_contained


def _command_object_move(current_line: str, **traits):
    syntax_full = r"MOVE OBJECT [\w_]*: [\w_]*"
    # MOVE OBJECT objectname: change_time, x_change, ...
    # ^^^^^^^^^^^^^^^^^^^^^^^~~~~~~~~~~~~~~~~~~~~~~~ ...
    if not re.match(syntax_full, current_line):
        # %&$ Raise exception for the script.
        raise UserWarning("SyntaxIssue: MOVE OBJECT keyword")

    MOVE_OBJECT_ = re.search("MOVE OBJECT ", current_line)
    # MOVE OBJECT objectname: move_time, x, y, ...
    # ^^^^^^^^^^^
    if MOVE_OBJECT_ is None:
        raise UserWarning("SyntaxIssue: MOVE OBJECT keyword; \'MOVE_OBJECT_\'.")

    colon = re.search(":", current_line)
    # MOVE OBJECT objectname: move_time, x, y, ...
    #                       ^
    if colon is None:
        raise UserWarning("SyntaxIssue: MOVE OBJECT keyword; \'colon\'.")

    object_name = _collect_syntax_snapshot(current_line, MOVE_OBJECT_, colon)
    # object_name = current_line[MOVE_OBJECT_.end():colon.start()]

    keys = _split_by_keys(current_line[colon.end():], 5)

    keys_contained = [
        "M",
        ["object_name", object_name],
        ["move_time", keys[0]],
        ["move_x", keys[1]],
        ["move_y", keys[2]],
        ["move_scale", keys[3]],
        ["move_rate", keys[4]]
    ]

    if len(keys) > 5:
        keys_contained = _split_extra_keys(keys_contained, keys[5:])

    keys_contained = _evaluate_values(keys_contained, **traits)

    return keys_contained


def _command_object_delete(current_line: str, **traits):
    syntax_full = r"DELETE OBJECT [\w_]*: [\w_]*"
    # DELETE OBJECT objectname: delete_time, ...
    # ^^^^^^^^^^^^^^^^^^^^^^^^^~~~~~~~~~~~~~ ...
    if not re.match(syntax_full, current_line):
        # %&$ Raise exception for the script.
        raise UserWarning("SyntaxIssue: DELETE OBJECT keyword")

    DELETE_OBJECT_ = re.search("DELETE OBJECT ", current_line)
    # DELETE OBJECT objectname: filename, start_time, ...
    # ^^^^^^^^^^^^^
    if DELETE_OBJECT_ is None:
        raise UserWarning("SyntaxIssue: DELETE OBJECT keyword; \'DELETE_OBJECT_\'.")

    colon = re.search(":", current_line)
    # DELETE OBJECT objectname: filename, start_time, ...
    #                         ^
    if colon is None:
        raise UserWarning("SyntaxIssue: DELETE OBJECT keyword; \'colon\'.")

    object_name = _collect_syntax_snapshot(current_line, DELETE_OBJECT_, colon)
    # object_name = current_line[DELETE_OBJECT_.end():colon.start()]

    keys = _split_by_keys(current_line[colon.end():], 1)

    keys_contained = [
        "D",
        ["object_name", object_name],
        ["delete_time", keys[0]]
    ]

    if len(keys) > 1:
        keys_contained = _split_extra_keys(keys_contained, keys[1:])

    keys_contained = _evaluate_values(keys_contained, **traits)

    return keys_contained


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


def _split_extra_keys(keys_contained: list, keys_series: list):
    for keys_item in keys_series:
        keys_contained.append(keys_item.split("=", 1))
        if len(keys_contained[-1]) != 2:
            raise UserWarning("Temporary exception for excess keys or multiple equal signs.")
        keys_contained[-1][0] = keys_contained[-1][0].lower()
    return keys_contained


def _evaluate_values(keys_contained: list, **traits):
    value_types = {
        "object_name": "STRING",
        "file_name": "ADDRESS",
        "start_time": "TIME",
        "x": "INT",
        "y": "INT",
        "scale": "FLOAT",
        "layer": "INT",
        "move_time": "TIME",
        "move_x": "INT",
        "move_y": "INT",
        "move_scale": "FLOAT",
        "move_rate": "TIME",
        "delete_time": "TIME",
        "delay": "TIME"  # optional
    }

    for index, (name, contents) in enumerate(keys_contained[1:].copy(), start=1):
        if value_types[name] == "STRING":
            continue

        if value_types[name] == "TIME":
            keys_contained[index][1] = _manage_time(contents, traits["_HEAD"]["frame_rate"])
            continue

        type_ = value_types[name]
        for key in traits[type_]:
            if contents.find(key) == -1:
                continue

            if type_ == "ADDRESS" and contents.find(key) != -1:
                keys_contained[index][1] = contents.replace(key + "/", traits[type_][key])
                continue

            keys_contained[index][1] = contents.replace(key, traits[type_][key])

        if type_ == "ADDRESS":
            continue

        if type_ == "INT":
            keys_contained[index][1] = int(keys_contained[index][1])
        elif type_ == "FLOAT":
            keys_contained[index][1] = float(keys_contained[index][1])
        elif type_ == "BOOL":
            keys_contained[index][1] = bool(keys_contained[index][1])

    return keys_contained
