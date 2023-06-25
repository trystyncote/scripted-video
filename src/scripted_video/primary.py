from src.scripted_video.utils import find_path_of_file, create_encoder, TemporaryDirectory
from src.scripted_video.compile_time import cycle_over_script
from src.scripted_video.FrameDraw import generate_frames, draw_frames, stitch_video

from src.scripted_video.variables.ScriptVariables import ScriptVariables

from scripted_video.qualms.force_exit import svForceExit

import logging
from pathlib import Path


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


def generate_script(script_file: Path, logger: logging.Logger):
    variables = ScriptVariables()
    variables.metadata.script_file = script_file
    encoder = create_encoder()

    logger.warning("Starting compiling the script.")

    object_information = cycle_over_script(script_file, variables)

    logger.warning("Completed compiling the script.")
    logger.warning("Started drawing the frames for the video.")

    frames = generate_frames(object_information, variables)

    dir = variables.metadata.script_file.parent / encoder
    with TemporaryDirectory(dir) as tempdir:
        video_length = draw_frames(frames, tempdir.dir, object_information)

        logger.warning("Completed drawing the frames for the video.")
        logger.warning("Started stitching the video together.")

        stitch_video(tempdir.dir, variables.metadata.file_name, video_length, variables.metadata.frame_rate)

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
    except svForceExit:
        input("")
