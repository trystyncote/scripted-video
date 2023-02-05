from File import find_path_of_file


def define_prefix(current_line: str, traits: dict):
    split_current_line = current_line.split(" ")

    if split_current_line[0].upper() == "HEAD":
        return tuple(_command_head(current_line))

    elif split_current_line[0] == "SET":
        return _command_set(current_line)

    elif split_current_line[1] == "OBJECT":
        if split_current_line[0] == "CREATE":
            return _command_object_create(current_line,
                                          frame_rate=traits["frame_rate"])

        elif split_current_line[0] == "MOVE":
            return _command_object_move(current_line,
                                        frame_rate=traits["frame_rate"])

        elif split_current_line[0] == "DELETE":
            return _command_object_delete(current_line,
                                          frame_rate=traits["frame_rate"])

    # %&$ Raise exception for the script.
    return None


def _discover_syntax(current_line: str, syntax: tuple):
    outstanding_single_quotes = False
    outstanding_double_quotes = False

    syntax_index = 0
    line_index = 0
    line_data = []

    for index, contents in enumerate(current_line):
        if not outstanding_single_quotes and contents == "\'":
            outstanding_single_quotes = True
            continue
        elif outstanding_single_quotes:
            if contents == "\'":
                outstanding_single_quotes = False
            continue

        if not outstanding_double_quotes and contents == "\"":
            outstanding_double_quotes = True
            continue
        elif outstanding_double_quotes:
            if contents == "\"":
                outstanding_double_quotes = False
            continue

        if (current_line[index:index+len(syntax[syntax_index])].upper()
                == syntax[syntax_index]):
            if syntax_index != 0:
                line_data.append(current_line[syntax_index:index])
            syntax_index = index + len(syntax[syntax_index])
            line_data.append(current_line[index:index+len(syntax[syntax_index])])

            while True:
                syntax_index += 1
                try:
                    if syntax[syntax_index][0] != "@":
                        break
                except IndexError:
                    break

            try:
                syntax[syntax_index]
            except IndexError:
                line_data.append(current_line[index+len(line_data[-1]):])
                break

    return line_data


def _manage_time(time_string: str, frame_rate: int):
    time_string = time_string.split(" ")
    _ = time_string.pop(-1)
    suffix_effect = {"f": 1,
                     "s": frame_rate,
                     "m": frame_rate*60,
                     "h": frame_rate*60*60}

    time = 0.0
    for i in time_string:
        time += float(i[:-1]) * suffix_effect[i[-1]]

    return int(time)


def _command_head(current_line: str):
    syntax = ("HEAD ", "@variable", "=", "@value")
    keyword_list = ["window_width", "window_height", "frame_rate", "file_name"]
    line_data = _discover_syntax(current_line, syntax)

    classify_variable = line_data[1]
    classify_value = line_data[3]
    try:
        classify_value = int(classify_value)
    except ValueError:
        pass

    for keyword in keyword_list:
        if keyword == classify_variable.lower():
            return classify_variable, classify_value

    # %&$ Raise exception for the script.
    return None


def _command_set(current_line: str, **traits):
    syntax = ("SET ", "@variable", "=", "@value", " AS ", "@type")
    line_data = _discover_syntax(current_line, syntax)

    classify_variable = line_data[1]
    classify_value = line_data[3]
    classify_type = line_data[5]

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
            classify_value = traits["file_name"]
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

    classify_object = line_data[1]
    classify_file_name = line_data[3]
    classify_initial_time = _manage_time(line_data[5], traits["frame_rate"])
    classify_x_coord = int(line_data[7])
    classify_y_coord = int(line_data[9])
    classify_scale = float(line_data[11])
    classify_layer = int(line_data[13])

    return "C", classify_object, classify_file_name, classify_initial_time, \
        classify_x_coord, classify_y_coord, classify_scale, classify_layer


def _command_object_move(current_line: str, **traits):
    syntax = ("MOVE OBJECT ", "@objectname", ":", "@changetime", ",",
              "@xchange", ",", "@ychange", ",", "@scale", ",", "@rate")
    line_data = _discover_syntax(current_line, syntax)

    classify_object = line_data[1]
    classify_change_time = _manage_time(line_data[3], traits["frame_rate"])
    classify_x_change = int(line_data[5])
    classify_y_change = int(line_data[7])
    classify_scale_change = float(line_data[9])
    classify_rate = _manage_time(line_data[11], traits["frame_rate"])

    return "M", classify_object, classify_change_time, classify_x_change, \
        classify_y_change, classify_scale_change, classify_rate


def _command_object_delete(current_line: str, **traits):
    syntax = ("DELETE OBJECT ", "@objectname", ":", "@deletetime", ",",
              "@delay")
    line_data = _discover_syntax(current_line, syntax)

    classify_object = line_data[1]
    classify_delete_time = _manage_time(line_data[3], traits["frame_rate"])
    classify_delay = _manage_time(line_data[5], traits["frame_rate"])

    return "D", classify_object, classify_delete_time, classify_delay
