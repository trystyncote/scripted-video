from enum import auto as enum_auto, Enum
from io import StringIO
from pathlib import Path


def _read_script(file_name: (Path | str)):
    with open(file_name, "r", encoding="utf-8") as file_pointer:
        for line in file_pointer:
            yield line


def _clear_line(string: str, start_index: int, end_index: int):
    return string[:start_index] + string[end_index:]


def _combine_previous_lines(*lines):
    combined = StringIO()
    for line in lines:
        if line.strip() == "":
            continue
        combined.write(line + " ")
    return combined.getvalue()


class _OutstandingState(Enum):
    empty = enum_auto()
    block_comment = enum_auto()


def script_parser(file: (Path | str), /, *,
                  block_comment_characters: tuple[str, str] | str | None = None, end_line_character: str = "\n",
                  inline_comment_character: str | None = None):
    if type(block_comment_characters) == str:
        block_comment_characters = (block_comment_characters, block_comment_characters)

    at_end_of_line = False
    index_block_comment_start = -1
    line_previous = []
    outstanding_state = _OutstandingState.empty
    script_pointer = _read_script(file)

    try:
        line_current = next(script_pointer)
    except StopIteration:
        return

    while script_pointer:
        if block_comment_characters:
            if outstanding_state is not _OutstandingState.block_comment:
                index_block_comment_start = line_current.find(block_comment_characters[0])
                if index_block_comment_start != -1:
                    outstanding_state = _OutstandingState.block_comment

            if outstanding_state is _OutstandingState.block_comment:
                index_block_comment_end = line_current.find(block_comment_characters[1], index_block_comment_start)
                if index_block_comment_end != -1:
                    outstanding_state = _OutstandingState.empty
                    length_block_end = len(block_comment_characters[1])
                    line_current = _clear_line(line_current, index_block_comment_start,
                                               index_block_comment_end+length_block_end)
                else:
                    line_current = _clear_line(line_current, index_block_comment_start, len(line_current))
                    index_block_comment_start = 0

        index_end_line = line_current.find(end_line_character)
        if index_end_line != -1:
            at_end_of_line = True
            line_current = line_current[:index_end_line]
        else:
            line_previous.append(line_current.strip())

        if inline_comment_character and outstanding_state is not _OutstandingState.block_comment:
            index_inline_comment = line_current.find(inline_comment_character)
            if index_inline_comment != -1:
                line_current = line_current[:index_inline_comment]

        line_current = line_current.strip()
        if at_end_of_line:
            if line_previous:
                yield _combine_previous_lines(*line_previous, line_current).strip()
                line_previous = []
            elif line_current:
                yield line_current

        try:
            line_current = next(script_pointer)
        except StopIteration:
            if line_previous:
                yield _combine_previous_lines(*line_previous).strip()
            return

        at_end_of_line = False
