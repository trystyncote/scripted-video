from src.scripted_video.File import find_path_of_file, create_encoder
from src.scripted_video.parser import script_parser
from src.scripted_video.compile_time import create_syntax_tree_root, dissect_syntax, navigate_syntax_tree
from src.scripted_video.FrameDraw import generate_frames, draw_frames, stitch_video

from src.scripted_video.variables.ScriptVariables import ScriptVariables

from src.scripted_video.objects.ObjectDict import ObjectDict

from scripted_video.qualms.force_exit import svForceExit

import logging
from pathlib import Path
import shutil


def detect_performance():
    # Code borrowed from mCoding. See the following link:
    # https://github.com/mCodingLLC/VideosSampleCode/blob/master/videos/063_find_why_your_python_code_is_slow_using_this_essential_tool_dot___feat_dot__async_await_/needs_profiling.py
    import cProfile
    import pstats

    script = Path(find_path_of_file("svDemo1.txt"))
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
    syntax_tree = create_syntax_tree_root(str(script_file.name))

    for line in script_parser(script_file, block_comment_characters=("/*", "*/"), end_line_character=";",
                              inline_comment_character="//"):
        dissect_syntax(line, syntax_tree)

    navigate_syntax_tree(syntax_tree, object_information, variables)

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
    try:
        primary()
        # detect_performance()
    except svForceExit:
        input("")
