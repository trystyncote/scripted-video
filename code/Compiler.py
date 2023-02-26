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
        h = _command_head(current_line)
        h = tuple(h)
        return h

    elif split_current_line[0] == "SET":
        return _command_set(current_line, **traits)

    elif split_current_line[1] == "OBJECT":
        if split_current_line[0] == "CREATE":
            return _command_object_create(current_line, **traits)

        elif split_current_line[0] == "MOVE":
            return _command_object_move(current_line, **traits)

        elif split_current_line[0] == "DELETE":
            return _command_object_delete(current_line, **traits)

    # %&$ Raise exception for the script.
    return None


def _update_line_data(line_data: list, current_line: str, start_index: int, end_index: int):
    line_data.append(current_line[start_index:end_index])
    # line_data[-1] = line_data[-1].split()[0]
    return line_data


def _discover_syntax(current_line: str, syntax: tuple):
    # These variables are to prevent a command from taking effect in the middle
    # of a string, when it's not supposed to.
    outstanding_single_quotes = False
    outstanding_double_quotes = False

    # The syntax has variable members ("@something") that are near-impossible
    # to track as-is, so the other members are used as *anchors* to guide the
    # rest.

    syntax_index = 0  # The purpose of syntax_index is to be a separate counter
    # to the index in the upcoming for-loop. In particular, syntax_index is
    # counting indexes of the syntax variable, as opposed to the current_line.
    line_index = 0
    line_data = []  # line_data is the list with the commands in them.

    for index, contents in enumerate(current_line):
        # Checks for outstanding single quotes (').
        if not outstanding_single_quotes and contents == "\'":
            outstanding_single_quotes = True
            continue
        elif outstanding_single_quotes:
            if contents == "\'":
                outstanding_single_quotes = False
            continue

        # Checks for outstanding double quotes (").
        if not outstanding_double_quotes and contents == "\"":
            outstanding_double_quotes = True
            continue
        elif outstanding_double_quotes:
            if contents == "\"":
                outstanding_double_quotes = False
            continue

        if (current_line[index:index+len(syntax[syntax_index])].upper()
                == syntax[syntax_index]):  # This line is looking for the
            # current member of the syntax, denoted by syntax_index. This helps
            # the program find the anchors for the syntax.
            if syntax_index != 0:
                # If the syntax_index is for the first element, then there is
                # no previous element, meaning the system doesn't collect it.
                # line_data.append(current_line[line_index:index])
                # line_data[-1] = line_data[-1].strip()
                line_data = _update_line_data(line_data, current_line,
                                              line_index, index)
            line_index = index + len(syntax[syntax_index])
            # line_data.append(current_line[index:index+len(syntax[syntax_index])])
            # line_data[-1] = line_data[-1].strip()
            line_data = _update_line_data(line_data, current_line, index,
                                          index+len(syntax[syntax_index]))

            # syntax_index needs to update by two to move to the next part of
            # the syntax that isn't a variable part (@something). No member of
            # syntax should have two variable parts in a row, or two
            # non-variable parts in a row. There needs be always a seperator
            # between variable parts, lest this code breaks.
            syntax_index += 2

            try:
                syntax[syntax_index]  # This statement just exists to raise an
                # IndexError if the syntax_index is out of range.
            except IndexError:
                # line_data.append(current_line[index+len(line_data[-1]):])
                # line_data[-1] = line_data[-1].split()
                line_data = _update_line_data(line_data, current_line,
                                              index+len(line_data[-1]),
                                              len(current_line))
                # The remainder of the current_line is pasted into the
                # line_data to allow it to exist. This usually takes everything
                # in the line after the previous anchor.
                break

    for index, contents in enumerate(line_data):
        line_data[index] = contents.split()[0]

    return line_data


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


def _collect_syntax_snapshot(full_line, re_match_instance: re.Match):
    return full_line[re_match_instance.start():re_match_instance.end()]


def _command_head(current_line: str):
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

    return keyword, contents


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
            classify_value = traits["_script_name"]
            classify_value = classify_value.rsplit("\\", 1)
            classify_value = classify_value[0] + "\\"

    else:
        # %&$ Raise exception for the script.
        pass

    return classify_variable, classify_value


def _command_object_create(current_line: str, **traits):
    # CREATE OBJECT @objectname: @filename, @initialtime, @x, @y, @scale, @layer
    syntax = ("CREATE OBJECT ", "@objectname", ":", "@filename", ",",
              "@initialtime", ",", "@x", ",", "@y", ",", "@scale", ",",
              "@layer")
    line_data = _discover_syntax(current_line, syntax)

    # These 'classify' grade variables are based on position, which is based on
    # syntax.
    classify_object = line_data[1]
    classify_file_name = line_data[3]
    classify_initial_time = _manage_time(line_data[5], traits["frame_rate"])
    classify_x_coord = int(line_data[7])
    classify_y_coord = int(line_data[9])
    classify_scale = float(line_data[11])
    classify_layer = int(line_data[13])

    # The "C" is to denote two things: first, that this is a result of the
    # OBJECT keyword family. Second, that among that family, this is for an
    # object's creation/initialization.
    return "C", classify_object, classify_file_name, classify_initial_time, \
        classify_x_coord, classify_y_coord, classify_scale, classify_layer


def _command_object_move(current_line: str, **traits):
    syntax = ("MOVE OBJECT ", "@objectname", ":", "@changetime", ",",
              "@xchange", ",", "@ychange", ",", "@scale", ",", "@rate")
    line_data = _discover_syntax(current_line, syntax)

    # These 'classify' grade variables are based on position, which is based on
    # syntax.
    classify_object = line_data[1]
    classify_change_time = _manage_time(line_data[3], traits["frame_rate"])
    classify_x_change = int(line_data[5])
    classify_y_change = int(line_data[7])
    classify_scale_change = float(line_data[9])
    classify_rate = _manage_time(line_data[11], traits["frame_rate"])

    # The "M" is to denote two things: first, that this is a result of the
    # OBJECT keyword family. Second, that among that family, this is for the
    # act of moving an object.
    return "M", classify_object, classify_change_time, classify_x_change, \
        classify_y_change, classify_scale_change, classify_rate


def _command_object_delete(current_line: str, **traits):
    syntax = ("DELETE OBJECT ", "@objectname", ":", "@deletetime", ",",
              "@delay")
    line_data = _discover_syntax(current_line, syntax)

    # These 'classify' grade variables are based on position, which is based on
    # syntax.
    classify_object = line_data[1]
    classify_delete_time = _manage_time(line_data[3], traits["frame_rate"])
    classify_delay = _manage_time(line_data[5], traits["frame_rate"])

    # The "D" is to denote two things: first, that this is a result of the
    # OBJECT keyword family. Second, that among that family, this is for an
    # object's deletion.
    return "D", classify_object, classify_delete_time, classify_delay
