from scripted_video.File import find_path_of_file, create_encoder
from scripted_video.Scripter import Scripter
from scripted_video.Compiler import define_prefix
from scripted_video.Timetable import create_timetable
from scripted_video.FrameDraw import create_video

import logging
from pathlib import Path


def primary():
    script_variables = {
        "_HEAD": {
            "_script_name":  "",
            "file_name":     "",
            "frame_rate":    0,
            "window_height": 0,
            "window_width":  0
        },
        "ADDRESS": {},
        "BOOL":    {},
        "FLOAT":   {},
        "INT":     {},
        "STRING":  {}
    }

    script_file = find_path_of_file("scriptedVideo_demoScript_1.txt")
    script = Scripter(Path(script_file))
    script_variables["_HEAD"]["_script_name"] = script_file

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
