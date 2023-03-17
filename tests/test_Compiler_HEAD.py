from scripted_video.Compiler import define_prefix
import pytest


def return_traits_example():
    return {
        "_HEAD": {
            "_script_name": "...",
            "file_name": None,
            "frame_rate": None,
            "window_width": None,
            "window_height": None
        }
    }


@pytest.mark.parametrize("test_input,keyword,expected",
    [("HEAD window_width = 852", "window_width", 852),
     ("HEAD window_height = 532", "window_height", 532),
     ("HEAD frame_rate = 24", "frame_rate", 24),
     ("HEAD file_name = file_result", "file_name", "file_result")]
)
def test_syntax_success(test_input, keyword, expected):
    # Tests for whether the syntax is successfully being dissected.
    result, _ = define_prefix(test_input, return_traits_example())
    assert result["_HEAD"][keyword] == expected


@pytest.mark.parametrize("test_input",
    ["HEAD windwo_width = 852",
     "HEAD window_hright = 532",
     "HEAD frame_rat = 24",
     "HEAD file_naem = file_result",
     "HEAD not a keyword = some_value"]
)
def test_syntax_failure_keyword(test_input):
    # Tests for whether a UserWarning is raised when the keyword is not proper.
    # This includes typos and keywords that don't exist.
    with pytest.raises(UserWarning):
        define_prefix(test_input, return_traits_example())


@pytest.mark.parametrize("test_input",
    ["HEAD window_width = ae",
     "HEAD window_height = ae",
     "HEAD frame_rate = af",
     "HEAD file_name = "]
)
def test_syntax_failure_value(test_input):
    # Tests for whether a UserWarning is raised when the wrong type of value
    # exists. This includes a string when an integer is expected, or when it
    # doesn't exist in the first place.
    with pytest.raises(ValueError):
        define_prefix(test_input, return_traits_example())
