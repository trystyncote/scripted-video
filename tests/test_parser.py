from src.scripted_video.File import find_path_of_file
from src.scripted_video.parser import script_parser


def test_parser_default():
    """ Tests the default behaviour of the `script_parser` function. """
    idx = 0
    expected = ["aAaA;", "bBbB;", "cCcC; // Commented out?", "dDdD", "eEeE;", "fFfF;", "gGgG; /*", "Commented out?",
                "*/", "hHhH", "i;"]
    for actual in script_parser(find_path_of_file("example_script_file_1.txt")):
        assert actual == expected[idx]
        idx += 1


def test_parser_inline_comments():
    """ Tests the ability to specify a prefix to inline comments. """
    idx = 0
    expected = ["aAaA;", "bBbB;", "cCcC;", "dDdD", "eEeE;", "fFfF;", "gGgG; /*", "Commented out?",
                "*/", "hHhH", "i;"]
    for actual in script_parser(find_path_of_file("example_script_file_1.txt"), inline_comment_character="//"):
        assert actual == expected[idx]
        idx += 1


def test_parser_block_comments():
    """ Tests the ability to specify a set of affixes to block comments. """
    idx = 0
    expected = ["aAaA;", "bBbB;", "cCcC; // Commented out?", "dDdD", "eEeE;", "fFfF;", "gGgG;", "hHhH", "i;"]
    for actual in script_parser(find_path_of_file("example_script_file_1.txt"), block_comment_characters=("/*", "*/")):
        assert actual == expected[idx]
        idx += 1


def test_parser_comments_both_types():
    """ Tests the compatibility of comments system when both are specified. """
    idx = 0
    expected = ["aAaA;", "bBbB;", "cCcC;", "dDdD", "eEeE;", "fFfF;", "gGgG;", "hHhH", "i;"]
    for actual in script_parser(find_path_of_file("example_script_file_1.txt"), block_comment_characters=("/*", "*/"),
                                inline_comment_character="//"):
        assert actual == expected[idx]
        idx += 1


def test_parser_end_line():
    """ Tests the specification of an end-line
        character that concludes a line.       """
    idx = 0
    expected = ["aAaA", "bBbB", "cCcC", "dDdD eEeE", "fFfF", "gGgG", "Commented out? */ hHhH i"]
    for actual in script_parser(find_path_of_file("example_script_file_1.txt"), end_line_character=";"):
        assert actual == expected[idx]
        idx += 1


def test_parser_end_line_with_comments():
    """ Tests the compatibility of an end-line
        character with both types of comments. """
    idx = 0
    expected = ["aAaA", "bBbB", "cCcC", "dDdD eEeE", "fFfF", "gGgG", "hHhH i"]
    for actual in script_parser(find_path_of_file("example_script_file_1.txt"), end_line_character=";",
                                block_comment_characters=("/*", "*/"), inline_comment_character="//"):
        assert actual == expected[idx]
        idx += 1
