from File import find_path_of_file, create_encoder
from Scripter import Scripter
from Compiler import define_prefix
from Timetable import create_timetable
from FrameDraw import create_video

import logging


def primary():
    script_traits = {"_script_name": find_path_of_file("sample_script.txt"),
                     "window_width": None,
                     "window_height": None,
                     "frame_rate": None,
                     "file_name": None}
    script = Scripter(script_traits["_script_name"])
    script_variables = {}
    timetable_information = []
    hold_value = None
    encoder = create_encoder()

    logging.basicConfig(format=">> %(message)s")
    l = logging.getLogger("")

    l.warning("Started reading script.")
    for _ in script:
        script.clear_comments()
        script.find_line_end()

        if not script.current_line:
            continue

        hold_value = define_prefix(script.current_line, script_traits)

        if len(hold_value) == 2:
            if hold_value[0] in script_traits:
                script_traits[hold_value[0]] = hold_value[1]
                continue

            script_variables[hold_value[0]] = hold_value[1]
            continue

        timetable_information.append(hold_value)

    l.warning("Finished reading script.")
    l.warning("Started creating the timetable.")

    sorted_timetable, object_information = create_timetable(
        timetable_information, script_variables
    )

    l.warning("Finished creating the timetable.")
    l.warning("Started drawing the frames for the video.")

    create_video(sorted_timetable, object_information, encoder, l, **script_traits)


if __name__ == "__main__":
    primary()
