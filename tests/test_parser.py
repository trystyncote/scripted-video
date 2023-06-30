from scripted_video.utils import find_path_of_file
from scripted_video.parser import script_parser

import pytest


@pytest.mark.parametrize("file,list_of_expected", [
    (find_path_of_file("example_script_file_1.txt"),
     ["aAaA;", "bBbB;", "cCcC; // Commented out?", "dDdD", "eEeE;", "fFfF;", "gGgG; /*", "Commented out?", "*/", "hHhH",
      "i;"]),
    (find_path_of_file("example_script_file_2.txt"),
     ["aAAaAA - bBBbBB { cCCcCC };", "dDDdDD;", "eEEeEE;", "// Commented out.", "fFFfFF;", "/* Commented out. */",
      "gGGgGG { hHHhHH { iIIiII; }; };"]),
    (find_path_of_file("example_script_file_3.txt"),
     ["aaaaA;", "-_-+-+-_-", "bbbbB;", "ccccC", "ddddD", "// Commented out.", "eeeeE;", "-_-+-+-_-",
      "ffffF (( ggggG; ), hhhhH /* Commented out. */ );", "[iiiiI];", "-_-+-+-_-", "jjjjJ;", "k;"])
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
      "gGGgGG { hHHhHH { iIIiII; }; };"]),
    (find_path_of_file("example_script_file_3.txt"), "//",
     ["aaaaA;", "-_-+-+-_-", "bbbbB;", "ccccC", "ddddD", "eeeeE;", "-_-+-+-_-",
      "ffffF (( ggggG; ), hhhhH /* Commented out. */ );", "[iiiiI];", "-_-+-+-_-", "jjjjJ;", "k;"])
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
      "gGGgGG { hHHhHH { iIIiII; }; };"]),
    (find_path_of_file("example_script_file_3.txt"), ("/*", "*/"),
     ["aaaaA;", "-_-+-+-_-", "bbbbB;", "ccccC", "ddddD", "// Commented out.", "eeeeE;", "-_-+-+-_-",
      "ffffF (( ggggG; ), hhhhH );", "[iiiiI];", "-_-+-+-_-", "jjjjJ;", "k;"])
])
def test_parser_block_comments(file, block_chars, list_of_expected):
    """ Tests the ability to specify a set of affixes to block comments. """
    for actual, expected in zip(script_parser(file, block_comment_characters=block_chars), list_of_expected):
        assert actual == expected


@pytest.mark.parametrize("file,inline_char,block_chars,list_of_expected", [
    (find_path_of_file("example_script_file_1.txt"), "//", ("/*", "*/"),
     ["aAaA;", "bBbB;", "cCcC;", "dDdD", "eEeE;", "fFfF;", "gGgG;", "hHhH", "i;"]),
    (find_path_of_file("example_script_file_2.txt"), "//", ("/*", "*/"),
     ["aAAaAA - bBBbBB { cCCcCC };", "dDDdDD;", "eEEeEE;", "fFFfFF;", "gGGgGG { hHHhHH { iIIiII; }; };"]),
    (find_path_of_file("example_script_file_3.txt"), "//", ("/*", "*/"),
     ["aaaaA;", "-_-+-+-_-", "bbbbB;", "ccccC", "ddddD", "eeeeE;", "-_-+-+-_-", "ffffF (( ggggG; ), hhhhH );",
      "[iiiiI];", "-_-+-+-_-", "jjjjJ;", "k;"])
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
      "/* Commented out. */ gGGgGG { hHHhHH { iIIiII; }; }"]),
    (find_path_of_file("example_script_file_3.txt"), ";",
     ["aaaaA", "-_-+-+-_- bbbbB", "ccccC ddddD // Commented out. eeeeE",
      "-_-+-+-_- ffffF (( ggggG; ), hhhhH /* Commented out. */ )", "[iiiiI]", "-_-+-+-_- jjjjJ", "k"])
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
     ["aAAaAA - bBBbBB { cCCcCC }", "dDDdDD", "eEEeEE", "fFFfFF", "gGGgGG { hHHhHH { iIIiII; }; }"]),
    (find_path_of_file("example_script_file_3.txt"), ";", "//", ("/*", "*/"),
     ["aaaaA", "-_-+-+-_- bbbbB", "ccccC ddddD eeeeE", "-_-+-+-_- ffffF (( ggggG; ), hhhhH )", "[iiiiI]",
      "-_-+-+-_- jjjjJ", "k"])
])
def test_parser_end_line_with_comments(file, end_line_char, inline_char, block_char, list_of_expected):
    """ Tests the compatibility of an end-line
        character with both types of comments. """
    for actual, expected in zip(script_parser(file, end_line_character=end_line_char,
                                              block_comment_characters=block_char,
                                              inline_comment_character=inline_char),
                                list_of_expected):
        assert actual == expected


@pytest.mark.parametrize("file,end_line_char,header_id,list_of_expected", [
    (find_path_of_file("example_script_file_3.txt"), ";", [(str.startswith, "-_-+-+-_-")],
     ["aaaaA", "-_-+-+-_-", "bbbbB", "ccccC ddddD // Commented out. eeeeE", "-_-+-+-_-",
      "ffffF (( ggggG; ), hhhhH /* Commented out. */ )", "[iiiiI]", "-_-+-+-_-", "jjjjJ", "k"])
])
def test_parser_header_identity(file, end_line_char, header_id, list_of_expected):
    """ Tests the usage of header_identity. """
    # This makes use of the end-line character because the header_identity
    # doesn't change the default behaviour on its own.
    for actual, expected in zip(script_parser(file, end_line_character=end_line_char, header_identity=header_id),
                                list_of_expected):
        assert actual == expected


@pytest.mark.parametrize("file,end_line_char,header_id,inline_char,block_char,list_of_expected", [
    (find_path_of_file("example_script_file_3.txt"), ";", [(str.startswith, "-_-+-+-_-")], "//", ("/*", "*/"),
     ["aaaaA", "-_-+-+-_-", "bbbbB", "ccccC ddddD eeeeE", "-_-+-+-_-", "ffffF (( ggggG; ), hhhhH )", "[iiiiI]",
      "-_-+-+-_-", "jjjjJ", "k"])
])
def test_parser_header_identity_with_comments(file, end_line_char, header_id, inline_char, block_char,
                                              list_of_expected):
    """ Tests the usage of header_identity
        with compatibility with comments. """
    # This makes use of the end-line character because the header_identity
    # doesn't change the default behaviour on its own.
    for actual, expected in zip(script_parser(file, block_comment_characters=block_char,
                                              end_line_character=end_line_char,
                                              inline_comment_character=inline_char, header_identity=header_id),
                                list_of_expected):
        assert actual == expected
