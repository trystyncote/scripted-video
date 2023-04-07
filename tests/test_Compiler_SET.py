from scripted_video.Compiler import define_prefix
import pytest


def return_traits_example():
    return {
        "_HEAD": {
            "_script_name": r"src\script\Script.txt",
            "file_name": None,
            "frame_rate": None,
            "window_width": None,
            "window_height": None
        },
        "ADDRESS": {},
        "BOOL":    {},
        "FLOAT":   {},
        "INT":     {},
        "STRING":  {}
    }


@pytest.mark.skip(reason="Functionality isn't set in stone.")
@pytest.mark.parametrize("test_input,keyword,var_type,expected", [
    ("SET hello_world = \"Hello, world!\" AS STRING", "hello_world", "STRING", "\"Hello, world!\""),
    ("SET addr = __current_address__ AS ADDRESS", "addr", "ADDRESS", "src\\script\\"),
    ("SET decimal = 0.45 AS FLOAT", "decimal", "FLOAT", 0.45),
    ("SET not_decimal = 3 AS INT", "not_decimal", "INT", 3),
    ("SET boolean = False AS BOOL", "boolean", "BOOL", False)
])
def test_syntax_success(test_input, keyword, var_type, expected):
    # Tests for whether the syntax is successfully being dissected.
    result, _ = define_prefix(test_input, return_traits_example())
    assert result[var_type][keyword] == expected


@pytest.mark.skip(reason="Functionality isn't set in stone.")
@pytest.mark.parametrize("test_input", [
    "SET variable = \"Hello, world!\" AS INT",
    "SET variable = \"Hello, world!\" AS FlOAT",
    "SET variable = \"Hello, world!\" AS BOOL"
])
def test_syntax_failure_value_error(test_input):
    with pytest.raises(ValueError):
        define_prefix(test_input, return_traits_example())


@pytest.mark.skip(reason="Functionality isn't set in stone.")
def test_syntax_failure_variable_type():
    test_input = "SET variable = \"Hello, world!\" AS NOTATYPE"
    with pytest.raises(UserWarning):
        define_prefix(test_input, return_traits_example())
