from src.scripted_video.File import find_path_of_file, create_encoder
from src.scripted_video.Scripter import Scripter
from src.scripted_video.Compiler import define_prefix
from src.scripted_video.Timetable import create_timetable
from src.scripted_video.FrameDraw import create_video

import logging


def primary():
    script_variables = {
        "_HEAD": {
            "_script_name":  None,
            "file_name":     None,
            "frame_rate":    None,
            "window_height": None,
            "window_width":  None
        },
        "ADDRESS": {},
        "BOOL":    {},
        "FLOAT":   {},
        "INT":     {},
        "STRING":  {}
    }

    script_file = find_path_of_file("scriptedvideo_sample_script_1.txt")
    script = Scripter(script_file)
    script_variables["_HEAD"]["_script_name"] = script_file

    timetable_information = []
    object_information = {}
    encoder = create_encoder()

    logging.basicConfig(format=">> %(message)s")
    l = logging.getLogger("")

    l.warning("Started reading script.")
    for _ in script:
        script.clear_comments()
        script.find_line_end()

        if not script.current_line:
            continue

        hold_value, classification = define_prefix(script.current_line, script_variables)  # 52:73, script_traits

        if classification == 1:
            script_variables = hold_value
            hold_value = None
            continue

        if classification == 2:
            timetable_information.append(hold_value)
            continue

        # More to come here?

    l.warning("Finished reading script.")
    l.warning("Started creating the timetable.")

    sorted_timetable, object_information = create_timetable(
        timetable_information, script_variables
    )

    l.warning("Finished creating the timetable.")
    l.warning("Started drawing the frames for the video.")

    create_video(sorted_timetable, object_information, encoder, l, **script_variables)


if __name__ == "__main__":
    primary()
