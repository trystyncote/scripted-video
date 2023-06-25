from src.scripted_video.utils import find_path_of_file, create_encoder, Options, TemporaryDirectory
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


def generate_script(script_file: Path, options: Options):
    variables = ScriptVariables()
    variables.metadata.script_file = script_file
    encoder = create_encoder()

    object_information = cycle_over_script(script_file, variables)
    if options.verbose:
        print(">> Completed compiling the script.")

    frames = generate_frames(object_information, variables)

    dir = variables.metadata.script_file.parent / encoder
    with TemporaryDirectory(dir) as tempdir:
        video_length = draw_frames(frames, tempdir.dir, object_information)
        stitch_video(tempdir.dir, variables.metadata.file_name, video_length, variables.metadata.frame_rate)

    if options.verbose:
        print(">> Completed stitching the video together.")


def primary():
    options = Options()
    options.verbose = False

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
