from src.scripted_video.File import find_path_of_file
from src.scripted_video.parser import script_parser

import pytest


@pytest.mark.parametrize("file,list_of_expected", [
    (find_path_of_file("example_script_file_1.txt"),
     ["aAaA;", "bBbB;", "cCcC; // Commented out?", "dDdD", "eEeE;", "fFfF;", "gGgG; /*", "Commented out?", "*/", "hHhH",
      "i;"]),
    (find_path_of_file("example_script_file_2.txt"),
     ["aAAaAA - bBBbBB { cCCcCC };", "dDDdDD;", "eEEeEE;", "// Commented out.", "fFFfFF;", "/* Commented out. */",
      "gGGgGG { hHHhHH { iIIiII; }; };"])
])
def test_parser_default(file, list_of_expected):
    """ Tests the default behaviour of the `script_parser` function. """
    for actual, expected in zip(script_parser(file), list_of_expected):
        assert actual == expected


@pytest.mark.parametrize("file,inline_char,list_of_expected", [
    (find_path_of_file("example_script_file_1.txt"), "//",
     ["aAaA;", "bBbB;", "cCcC;", "dDdD", "eEeE;", "fFfF;", "gGgG; /*", "Commented out?", "*/", "hHhH", "i;"]),
    (find_path_of_file("example_script_file_2.txt"), "//",
     ["aAAaAA - bBBbBB { cCCcCC };", "dDDdDD;", "eEEeEE;", "fFFfFF;", "/* Commented out. */",
      "gGGgGG { hHHhHH { iIIiII; }; };"])
])
def test_parser_inline_comments(file, inline_char, list_of_expected):
    """ Tests the ability to specify a prefix to inline comments. """
    for actual, expected in zip(script_parser(file, inline_comment_character=inline_char), list_of_expected):
        assert actual == expected


@pytest.mark.parametrize("file,block_chars,list_of_expected", [
    (find_path_of_file("example_script_file_1.txt"), ("/*", "*/"),
     ["aAaA;", "bBbB;", "cCcC; // Commented out?", "dDdD", "eEeE;", "fFfF;", "gGgG;", "hHhH", "i;"]),
    (find_path_of_file("example_script_file_2.txt"), ("/*", "*/"),
     ["aAAaAA - bBBbBB { cCCcCC };", "dDDdDD;", "eEEeEE;", "// Commented out.", "fFFfFF;",
      "gGGgGG { hHHhHH { iIIiII; }; };"])
])
def test_parser_block_comments(file, block_chars, list_of_expected):
    """ Tests the ability to specify a set of affixes to block comments. """
    for actual, expected in zip(script_parser(file, block_comment_characters=block_chars), list_of_expected):
        assert actual == expected


@pytest.mark.parametrize("file,inline_char,block_chars,list_of_expected", [
    (find_path_of_file("example_script_file_1.txt"), "//", ("/*", "*/"),
     ["aAaA;", "bBbB;", "cCcC;", "dDdD", "eEeE;", "fFfF;", "gGgG;", "hHhH", "i;"]),
    (find_path_of_file("example_script_file_2.txt"), "//", ("/*", "*/"),
     ["aAAaAA - bBBbBB { cCCcCC };", "dDDdDD;", "eEEeEE;", "fFFfFF;", "gGGgGG { hHHhHH { iIIiII; }; };"])
])
def test_parser_comments_both_types(file, inline_char, block_chars, list_of_expected):
    """ Tests the ability to specify a set of affixes to block comments. """
    for actual, expected in zip(script_parser(file, block_comment_characters=block_chars,
                                              inline_comment_character=inline_char),
                                list_of_expected):
        assert actual == expected


@pytest.mark.parametrize("file,end_line_char,list_of_expected", [
    (find_path_of_file("example_script_file_1.txt"), ";",
     ["aAaA", "bBbB", "cCcC", "dDdD eEeE", "fFfF", "gGgG", "Commented out? */ hHhH i"]),
    (find_path_of_file("example_script_file_2.txt"), ";",
     ["aAAaAA - bBBbBB { cCCcCC }", "dDDdDD", "eEEeEE", "// Commented out. fFFfFF",
      "/* Commented out. */ gGGgGG { hHHhHH { iIIiII; }; }"])
])
def test_parser_end_line(file, end_line_char, list_of_expected):
    """ Tests the specification of an end-line
        character that concludes a line.       """
    for actual, expected in zip(script_parser(file, end_line_character=end_line_char), list_of_expected):
        assert actual == expected


@pytest.mark.parametrize("file,end_line_char,inline_char,block_char,list_of_expected", [
    (find_path_of_file("example_script_file_1.txt"), ";", "//", ("/*", "*/"),
     ["aAaA", "bBbB", "cCcC", "dDdD eEeE", "fFfF", "gGgG", "hHhH i"]),
    (find_path_of_file("example_script_file_2.txt"), ";", "//", ("/*", "*/"),
     ["aAAaAA - bBBbBB { cCCcCC }", "dDDdDD", "eEEeEE", "fFFfFF", "gGGgGG { hHHhHH { iIIiII; }; }"])
])
def test_parser_end_line_with_comments(file, end_line_char, inline_char, block_char, list_of_expected):
    """ Tests the compatibility of an end-line
        character with both types of comments. """
    for actual, expected in zip(script_parser(file, end_line_character=end_line_char,
                                              block_comment_characters=block_char,
                                              inline_comment_character=inline_char),
                                list_of_expected):
        assert actual == expected
