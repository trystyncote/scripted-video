from __future__ import annotations

from enum import auto as enum_auto, Enum
from io import StringIO
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path


class svParserError(SyntaxError):
    pass


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


def _evaluate_block_comments(line_current, block_comment_characters, index_block_comment_start, nesting_status):
    if nesting_status.latest_nesting is not _NestingState.block_comment:
        index_block_comment_start = line_current.find(block_comment_characters[0])
        if index_block_comment_start != -1:
            nesting_status.increase_nesting(_NestingState.block_comment)

    if nesting_status.latest_nesting is _NestingState.block_comment:
        index_block_comment_end = line_current.find(block_comment_characters[1], index_block_comment_start)
        if index_block_comment_end != -1:
            nesting_status.decrease_nesting()
            length_block_end = len(block_comment_characters[1])
            line_current = _clear_line(line_current, index_block_comment_start,
                                       index_block_comment_end + length_block_end)
        else:
            line_current = _clear_line(line_current, index_block_comment_start, len(line_current))
            index_block_comment_start = 0

    return line_current, index_block_comment_start


def _evaluate_header_identity(line_current, header_identity):
    for callable_, parameter in header_identity:
        if callable_(line_current, parameter):
            return True
    return False


def _evaluate_wrappers(line_current, nesting_status):
    base_index = 0
    nesting_elements = [
        _NestingElements(_NestingState.parenthesis, "(", ")"),
        _NestingElements(_NestingState.brackets, "[", "]"),
        _NestingElements(_NestingState.braces, "{", "}")
    ]
    element_effect = {
        # char: (open/close, nesting_elements[index], _NestingState.STATE),
        "(": ("open", 0, _NestingState.parenthesis),
        ")": ("close", 0, _NestingState.parenthesis),
        "[": ("open", 1, _NestingState.brackets),
        "]": ("close", 1, _NestingState.brackets),
        "{": ("open", 2, _NestingState.braces),
        "}": ("close", 2, _NestingState.braces)
    }

    while True:
        for nesting_element in nesting_elements:
            nesting_element.find_open(line_current, base_index)
            nesting_element.find_close(line_current, base_index)

        open_index_series = [x.index_open for x in nesting_elements if x.index_open != -1]
        close_index_series = [x.index_close for x in nesting_elements if x.index_close != -1]
        index_series = [*open_index_series, *close_index_series]
        if not index_series:
            return

        base_index = min(index_series)
        base_index_element = line_current[base_index:base_index+1]
        direction, nesting_index, status = element_effect[base_index_element]
        if direction == "open":
            nesting_status.increase_nesting(status)
        elif direction == "close":
            if status != nesting_status.latest_nesting:
                raise svParserError
            nesting_status.decrease_nesting()

        base_index += 1


class _NestingElements:
    __slots__ = ("closing", "index_close", "index_open", "opening", "state")

    def __init__(self, state, opening, closing):
        self.state = state
        self.opening = opening
        self.closing = closing
        self.index_close = 0
        self.index_open = 0

    def find_close(self, line_current, base_index):
        self.index_close = line_current.find(self.closing, base_index)

    def find_open(self, line_current, base_index):
        self.index_open = line_current.find(self.opening, base_index)


class _NestingStatus:
    __slots__ = ("_stack",)

    def __init__(self):
        self._stack = []

    @property
    def is_not_nested(self):
        return not self._stack

    @property
    def latest_nesting(self):
        if not self._stack:
            return None
        else:
            return self._stack[-1]

    @property
    def has_wrappers(self):
        return _NestingState.parenthesis in self._stack or _NestingState.brackets in self._stack \
            or _NestingState.braces in self._stack

    def increase_nesting(self, layer):
        self._stack.append(layer)

    def decrease_nesting(self):
        _ = self._stack.pop(-1)


class _NestingState(Enum):
    empty = enum_auto()
    block_comment = enum_auto()
    parenthesis = enum_auto()
    brackets = enum_auto()
    braces = enum_auto()


def script_parser(file: (Path | str), /, *,
                  block_comment_characters: tuple[str, str] | str | None = None, end_line_character: str = "\n",
                  header_identity=None, inline_comment_character: str | None = None):
    """
    script_parser parses a text file and dissects its immediate syntax.

    :param file: Required. The file to be parsed.
    :param block_comment_characters: Optional. The character sequence(s)
        signifying a block comment. Should be provided as a length-2 tuple with
        two strings (beginning, end), or as a string (used for both sides).
    :param end_line_character: Optional. The character(s) used to signify the
        end of a line. Default is the new-line character.
    :param header_identity: Optional. A length-2 tuple, where the first element
        is a callable from the built-in string, and the second is the sequence
        to be passed in. Designed to be compatible with str.startswith.
    :param inline_comment_character: Optional. The character(s) signifying an
        inline comment.
    :return: Yields each line in the order of the file.
    """
    if type(block_comment_characters) is str:
        block_comment_characters = (block_comment_characters, block_comment_characters)

    at_end_of_line = False
    index_block_comment_start = -1
    line_previous = []
    nesting_status = _NestingStatus()
    script_pointer = _read_script(file)

    try:
        line_current = next(script_pointer)
    except StopIteration:
        return

    while script_pointer:
        if block_comment_characters:
            line_current, index_block_comment_start = _evaluate_block_comments(line_current, block_comment_characters,
                                                                               index_block_comment_start,
                                                                               nesting_status)

        if nesting_status.latest_nesting is not _NestingState.block_comment:
            _evaluate_wrappers(line_current, nesting_status)

        if header_identity and not nesting_status.has_wrappers \
                and _evaluate_header_identity(line_current, header_identity):
            at_end_of_line = True

        if not nesting_status.has_wrappers:
            index_end_line = line_current.find(end_line_character)
            if index_end_line != -1:
                at_end_of_line = True
                line_current = line_current[:index_end_line]

        if inline_comment_character and nesting_status.latest_nesting is not _NestingState.block_comment:
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
        else:
            line_previous.append(line_current)

        try:
            line_current = next(script_pointer)
        except StopIteration:
            if line_previous:
                yield _combine_previous_lines(*line_previous).strip()
            return

        at_end_of_line = False
