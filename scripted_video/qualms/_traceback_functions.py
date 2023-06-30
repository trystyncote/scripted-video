def _tweak_pinpoint_string(string: str, char: str, start: int, end: int) -> str:
    for idx in range(start, end):
        string = string[:idx] + char + string[idx:]
    return string


def write_border_mid(length: int, index: int) -> str:
    split_length = (length - 3) // 2
    dash_bundle = split_length * "-"
    return f"{dash_bundle} {index} {dash_bundle}"


def write_border_top(length: int) -> str:
    return f"+{length * '-'}"


def write_cause_line(cause_line: str) -> str:
    return cause_line


def write_header(cls_type: str, cls_name: str, line_number: int | None = None, file_name: str | None = None) -> str:
    if file_name is not None and line_number is not None:
        return f":{cls_type}: {cls_name}, line {line_number} in file {file_name}"
    elif file_name is not None:
        return f":{cls_type}: {cls_name}, in file {file_name}"
    elif line_number is not None:
        return f":{cls_type}: {cls_name}, line {line_number}"
    else:
        return f":{cls_type}: {cls_name}"


def write_message(message: str) -> str:
    return f"{' '*2}{message}"


def write_pinpoint(pinpoint_tuple, error_line_length: int) -> str:
    match pinpoint_tuple:
        case ((_, _), (_, _)):
            direct = pinpoint_tuple[0]
            loose = pinpoint_tuple[1]
        case (_, _):
            direct = pinpoint_tuple
            loose = None
        case _:
            return ""

    pinpoint_string = " " * error_line_length

    if loose is not None:
        pinpoint_string = _tweak_pinpoint_string(pinpoint_string, "~", loose[0], loose[1])
    pinpoint_string = _tweak_pinpoint_string(pinpoint_string, "^", direct[0], direct[1])
    return pinpoint_string
