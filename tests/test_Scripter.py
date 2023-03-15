from scripted_video.Scripter import Scripter
import pytest


def script_output(file_name):
    script = Scripter(file_name)
    string_output = ""

    for current_line in script:
        string_output += f"{{{current_line}}}"
    return string_output


def test_iteration():
    # Tests for the iteration of the script.
    assert script_output("example_script_file_1.txt") == "{aAaA;}{bBbB;}{cCcC;}{dDdD}{eEeE;}{}{fFfF;}{gGgG; /*}" \
           + "{Commented out?}{*/}{}{hHhH}{i;}"


def script_output_enumerate(file_name):
    script = Scripter(file_name)
    string_output = ""

    for index, current_line in enumerate(script):
        string_output += f"{{{index}, {current_line}}}"
    return string_output


def test_iteration_enumerate():
    # Tests for the iteration of the script, where the enumerate function is
    # used for the Scripter class.
    assert script_output_enumerate("example_script_file_1.txt") == "{0, aAaA;}{1, bBbB;}{2, cCcC;}{3, dDdD}{4, eEeE;}" \
           + "{5, }{6, fFfF;}{7, gGgG; /*}{8, Commented out?}{9, */}{10, }{11, hHhH}{12, i;}"


def script_output_comment_clearing(file_name):
    script = Scripter(file_name)
    string_output = ""
    new_current_line = None

    for current_line in script:
        script.clear_comments()
        new_current_line = script.current_line
        string_output += f"{{{new_current_line}}}"
    return string_output


def test_comment_clearing():
    # Tests for whether the script is correctly clearing comments when it's
    # called to.
    assert script_output_comment_clearing("example_script_file_1.txt") == "{aAaA;}{bBbB;}{cCcC;}{dDdD}{eEeE;}{}" \
           + "{fFfF;}{gGgG; }{}{}{}{hHhH}{i;}"


def script_output_end_line_detection(file_name):
    script = Scripter(file_name)
    string_output = ""
    new_current_line = None

    for current_line in script:
        script.find_line_end()
        new_current_line = script.current_line
        if not new_current_line:
            continue
        string_output += f"{{{new_current_line}}}"
    return string_output


def test_end_line_detection():
    # Tests for whether the script is correctly detecting the end-line
    # character when it's called to.
    assert script_output_end_line_detection("example_script_file_1.txt") == "{aAaA}{bBbB}{cCcC}{dDdD eEeE}{fFfF}" \
           + "{gGgG /*}{Commented out? */ hHhH i}"


@pytest.skip(reason="No assert statements.")
def test_repeating_iterating_false():
    # Tests for the behaviour if the script is being read twice, when it has
    # *not* been allowed to.
    pass


@pytest.skip(reason="No assert statements.")
def test_repeating_iterating_true():
    # Tests for the behaviour if the script is being read twice, when it *is*
    # allowed to.
    pass
