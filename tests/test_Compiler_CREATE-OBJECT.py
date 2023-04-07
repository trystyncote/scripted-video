from scripted_video.Compiler import define_prefix
import pytest


def return_traits_example():
    return {
        "_HEAD": {
            "_script_name":  r"src\script\Script.txt",
            "file_name":     "Script_final",
            "frame_rate":    24,
            "window_width":  800,
            "window_height": 600
        },
        "ADDRESS": {
            "addr": "src\\Images\\"
        },
        "BOOL":    {},
        "FLOAT":   {},
        "INT":     {},
        "STRING":  {}
    }


def return_keys_contained_expected(object_name, file_name, start_time, x, y, scale, layer):
    return [
        "C",
        ["object_name", object_name],
        ["file_name", file_name],
        ["start_time", start_time],
        ["x", x],
        ["y", y],
        ["scale", scale],
        ["layer", layer]
    ]


@pytest.mark.skip(reason="Functionality isn't set in stone.")
@pytest.mark.parametrize("test_input,keys_list", [
    ("CREATE OBJECT obj1: addr/img1.png, 0s, 0, 0, 1, 1",
     ("obj1", r"src\Images\img1.png", 0, 0, 0, 1.0, 1)),
    ("CREATE OBJECT obj2: img2.png, 0.5s, 100, 100, 1.0, 2",
     ("obj2", "img2.png", 12, 100, 100, 1.0, 2)),
    ("CREATE OBJECT obj3: src\\Images\\img3.png, 24f, 0, 0, 0.8, 3",
     ("obj3", r"src\Images\img3.png", 24, 0, 0, 0.8, 3)),
    ("CREATE OBJECT obj4: addr/img4.png, 1m, 0, 0, 1, 4",
     ("obj4", r"src\Images\img4.png", 1440, 0, 0, 1.0, 4)),
    ("CREATE OBJECT obj5: addr/img5.png, 1h, 0, 0, 1, 5",
     ("obj5", r"src\Images\img5.png", 86_400, 0, 0, 1.0, 5))
])
def test_syntax_success(test_input, keys_list):
    result, _ = define_prefix(test_input, return_traits_example())
    assert result == return_keys_contained_expected(*keys_list)
