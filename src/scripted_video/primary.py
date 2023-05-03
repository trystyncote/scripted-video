from src.scripted_video.File import find_path_of_file, create_encoder
from src.scripted_video.Scripter import Scripter
from src.scripted_video.Compiler import define_prefix
from src.scripted_video.Timetable import create_timetable
from src.scripted_video.FrameDraw import create_video

from src.scripted_video.variables.ScriptVariables import ScriptVariables

import logging
from pathlib import Path


def detect_performance():
    # Code borrowed from mCoding. See the following link:
    # https://github.com/mCodingLLC/VideosSampleCode/blob/master/videos/063_find_why_your_python_code_is_slow_using_this_essential_tool_dot___feat_dot__async_await_/needs_profiling.py
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        primary()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    # stats.dump_stats(filename='needs_profiling.prof')


def primary():
    script_variables = ScriptVariables()

    logging.basicConfig(format=">> %(message)s")
    log_master = logging.getLogger("")
    log_master.warning("Starting looking for the script file.")

    script_file = find_path_of_file("scriptedVideo_demoScript_1.txt")
    script = Scripter(Path(script_file))
    script_variables.metadata.script_name = script_file

    timetable_information = []
    object_information = {}
    encoder = create_encoder()

    log_master.warning("Finished looking for the script file.")
    log_master.warning("Started reading script.")

    for _ in script:
        script.clear_comments()
        script.find_line_end()

        if not script.current_line:
            continue

        hold_value, classification = define_prefix(script.current_line, script_variables)

        if classification == 2:
            timetable_information.append(hold_value)

        hold_value = None
        # More to come here?

    log_master.warning("Finished reading script.")
    log_master.warning("Started creating the timetable.")

    sorted_timetable, object_information = create_timetable(timetable_information)

    log_master.warning("Finished creating the timetable.")
    log_master.warning("Started drawing the frames for the video.")

    create_video(sorted_timetable, object_information, encoder, log_master, script_variables)


if __name__ == "__main__":
    primary()
    # detect_performance()
