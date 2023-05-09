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

    script = Path(find_path_of_file("scriptedVideo_demoScript_1.txt"))
    logging.basicConfig(">> %(message)s")
    logger = logging.getLogger("")

    with cProfile.Profile() as pr:
        generate_script(script, logger)

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()


def receive_input(logger):
    while True:
        input_response = input("")
        if input_response == "":
            return None
        logger.warning(f"Searching for file '{input_response}'.")
        try:
            file_path = find_path_of_file(input_response)
        except FileNotFoundError:
            logger.warning("Cannot find file. Try again.")
        else:
            logger.warning("Found the file!")
            return file_path


def cycle_over_script(script_file: Path, variables: ScriptVariables):
    timetable_information = []

    for line in Scripter(script_file, auto_clear_comments=True, auto_clear_end_line=True):
        hold_value, classification = define_prefix(line, variables)
        if classification == 2:
            timetable_information.append(hold_value)

        hold_value = None

    return timetable_information


def generate_script(script_file: Path, logger: logging.Logger):
    variables = ScriptVariables()
    variables.metadata.script_name = script_file

    encoder = create_encoder()
    # object_information = ObjectDict()

    logger.warning("Starting compiling the script.")

    timetable_information = cycle_over_script(script_file, variables)

    logger.warning("Completed compiling the script.")
    logger.warning("Started creating the timetable.")

    sorted_timetable, object_information = create_timetable(timetable_information)

    logger.warning("Completed creating the timetable.")
    logger.warning("Started drawing the frames for the video.")

    create_video(sorted_timetable, object_information, encoder, logger, variables)


def primary():
    logging.basicConfig(format=">> %(message)s")
    logger = logging.getLogger("")

    while True:
        logger.warning("Please input the name of your script. [To exit, leave blank.]")
        script = receive_input(logger)
        if script is None:
            break
        script = Path(script)

        logger.warning(f"Started generating the script for '{script.name}'")
        generate_script(script, logger)

    logger.warning("Goodbye :)")


if __name__ == "__main__":
    primary()
    # detect_performance()
