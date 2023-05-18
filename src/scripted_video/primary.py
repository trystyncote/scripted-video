from src.scripted_video.File import find_path_of_file, create_encoder
from src.scripted_video.Scripter import Scripter
from src.scripted_video.Compiler import define_prefix
from src.scripted_video.FrameDraw import generate_frames, draw_frames, stitch_video

from src.scripted_video.variables.ScriptVariables import ScriptVariables

from src.scripted_video.objects.ObjectDict import ObjectDict

import logging
from pathlib import Path
import shutil


def detect_performance():
    # Code borrowed from mCoding. See the following link:
    # https://github.com/mCodingLLC/VideosSampleCode/blob/master/videos/063_find_why_your_python_code_is_slow_using_this_essential_tool_dot___feat_dot__async_await_/needs_profiling.py
    import cProfile
    import pstats

    script = Path(find_path_of_file("scriptedVideo_demoScript_1.txt"))
    logging.basicConfig(format=">> %(message)s")
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
    object_information = ObjectDict()

    for line in Scripter(script_file, auto_clear_comments=True, auto_clear_end_line=True):
        define_prefix(line, variables, object_information)

    return object_information


def generate_script(script_file: Path, logger: logging.Logger):
    variables = ScriptVariables()
    variables.metadata.script_file = script_file
    encoder = create_encoder()

    logger.warning("Starting compiling the script.")

    object_information = cycle_over_script(script_file, variables)

    logger.warning("Completed compiling the script.")
    logger.warning("Started drawing the frames for the video.")

    frames = generate_frames(object_information, variables)
    folder_location, video_length = draw_frames(frames, encoder, object_information, variables)

    logger.warning("Completed drawing the frames for the video.")
    logger.warning("Started stitching the video together.")

    stitch_video(folder_location, variables.metadata.file_name, video_length, variables.metadata.frame_rate)
    shutil.rmtree(folder_location)

    logger.warning("Completed stitching the video together.")
    logger.warning(f"The video from '{script_file.name}' is done generating.")


def primary():
    logging.basicConfig(format=">> %(message)s")
    logger = logging.getLogger("")

    while True:
        logger.warning("Please input the name of your script. [To exit, leave blank.]")
        script = receive_input(logger)
        if script is None:
            break
        script = Path(script)

        logger.warning(f"Started generating the video for '{script.name}'")
        generate_script(script, logger)

    logger.warning("Goodbye :)")


if __name__ == "__main__":
    primary()
    # detect_performance()
