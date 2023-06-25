from src.scripted_video.utils import find_path_of_file, create_encoder, TemporaryDirectory
from src.scripted_video.compile_time import cycle_over_script
from src.scripted_video.FrameDraw import generate_frames, draw_frames, stitch_video

from src.scripted_video.variables.ScriptVariables import ScriptVariables

from scripted_video.qualms.force_exit import svForceExit

from pathlib import Path


def receive_input():
    while True:
        input_response = input("")
        if input_response == "":
            return None
        print(f">> Searching for file '{input_response}'.")
        try:
            file_path = find_path_of_file(input_response)
        except FileNotFoundError:
            print("  >> Cannot find file. Try again.")
        else:
            print("  >> Found the file!")
            return file_path


def generate_script(script_file: Path):
    variables = ScriptVariables()
    variables.metadata.script_file = script_file
    encoder = create_encoder()

    print(">> Starting compiling the script.")

    object_information = cycle_over_script(script_file, variables)

    print(">> Completed compiling the script.")
    print(">> Started drawing the frames for the video.")

    frames = generate_frames(object_information, variables)

    dir = variables.metadata.script_file.parent / encoder
    with TemporaryDirectory(dir) as tempdir:
        video_length = draw_frames(frames, tempdir.dir, object_information)

        print(">> Completed drawing the frames for the video.")
        print(">> Started stitching the video together.")

        stitch_video(tempdir.dir, variables.metadata.file_name, video_length, variables.metadata.frame_rate)

    print(">> Completed stitching the video together.")
    print(f">> The video from '{script_file.name}' is done generating.")


def primary():
    while True:
        print("Please input the name of your script. [To exit, leave blank.]")
        script = receive_input()
        if script is None:
            break
        script = Path(script)

        print(f">> Started generating the video for '{script.name}'")
        generate_script(script)

    print("Goodbye :)")


if __name__ == "__main__":
    try:
        primary()
    except svForceExit:
        input("")
