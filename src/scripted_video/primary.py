from src.scripted_video.File import find_path_of_file, create_encoder
from src.scripted_video.Scripter import Scripter
from src.scripted_video.Compiler import define_prefix
from src.scripted_video.Timetable import create_timetable
from src.scripted_video.FrameDraw import create_video

import logging
import pathlib


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

    script_file = pathlib.Path(find_path_of_file("scriptedvideo_sample_script_1.txt"))
    script = Scripter(str(script_file))
    script_variables["_HEAD"]["_script_name"] = script_file
    # pathlib.Path("dir").name for getting purely the root file name.

    timetable_information = []
    object_information = {}
    encoder = create_encoder()

    logging.basicConfig(format=">> %(message)s")
    log_master = logging.getLogger("")

    log_master.warning("Started reading script.")
    for _ in script:
        script.clear_comments()
        script.find_line_end()

        if not script.current_line:
            continue

        hold_value, classification = define_prefix(script.current_line, script_variables)

        if classification == 1:
            script_variables = hold_value

        if classification == 2:
            timetable_information.append(hold_value)

        hold_value = None
        # More to come here?

    log_master.warning("Finished reading script.")
    log_master.warning("Started creating the timetable.")

    sorted_timetable, object_information = create_timetable(
        timetable_information, script_variables
    )

    log_master.warning("Finished creating the timetable.")
    log_master.warning("Started drawing the frames for the video.")

    create_video(sorted_timetable, object_information, encoder, log_master, **script_variables)


if __name__ == "__main__":
    primary()