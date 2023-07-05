from scripted_video.variables.ScriptVariables import ScriptVariables

from pathlib import Path
import pytest


def test_variables_metadata_empty():
    metadata = ScriptVariables().metadata

    assert metadata.script_file is None
    assert metadata.file_name is None
    assert metadata.frame_rate is None
    assert metadata.window_height is None
    assert metadata.window_width is None


def test_variables_metadata_specified():
    metadata = ScriptVariables().metadata

    metadata.script_file = "ScriptFile"
    assert metadata.script_file == "ScriptFile"

    metadata.file_name = "FileName"
    assert metadata.file_name == "FileName"

    metadata.frame_rate = 24
    assert metadata.frame_rate == 24

    metadata.window_height = 600
    assert metadata.window_height == 600

    metadata.window_width = 800
    assert metadata.window_width == 800


def test_variables_metadata_script_file_twice():
    metadata = ScriptVariables().metadata

    metadata.script_file = "ScriptFile1"
    with pytest.raises(AttributeError):
        metadata.script_file = "ScriptFile2"


@pytest.mark.parametrize("type_,value,expected", [
    ("ADDRESS", "some/path", Path("some", "path")),
    ("ADDRESS", Path("this", "path"), Path("this/path")),
    ("BOOL", "TrUe", True),
    ("BOOL", "fAlSe", False),
    ("FLOAT", 10.5, 10.5),
    ("FLOAT", 4, 4.0),
    ("INT", 1, 1),
    ("STRING", "String", "String")
])
def test_variables_constants(type_, value, expected):
    constants_of_type = ScriptVariables().constants.call_relevant(type_)

    constants_of_type.create_variable("var", value)
    constants_of_type.get_variable("var")
    assert constants_of_type.get_variable("var") == expected


@pytest.mark.parametrize("type_,value", [
    ("ADDRESS", 100),
    ("BOOL", "Invalid"),
    ("FLOAT", "actually_string"),
    ("INT", "actually_string"),
    ("STRING", 100),
])
def test_variables_constants_mismatched(type_, value):
    constants_of_type = ScriptVariables().constants.call_relevant(type_)

    with pytest.raises(AttributeError):
        constants_of_type.create_variable("var", value)
