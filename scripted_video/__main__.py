from .compile_time import cycle_over_script
from .FrameDraw import draw_frames, generate_frames, stitch_video
from .utils import create_encoder, find_path_of_file, Options, TemporaryDirectory

from .qualms.force_exit import svForceExit

from .variables.ScriptVariables import ScriptVariables

import argparse
from pathlib import Path


def end_program():
    import sys
    sys.exit(1)


def generate_script(script_file: Path, options: Options):
    variables = ScriptVariables()
    variables.metadata.script_file = script_file

    object_information = cycle_over_script(script_file, variables, options)
    if options.verbose:
        print("Completed compiling the script.")
    elif options.debug:
        print(":: All collected ImageObject instances.")
        for obj in object_information.values():
            print(repr(obj))
        print("")

    frames = generate_frames(object_information, variables)

    directory = variables.metadata.script_file.parent / create_encoder()
    with TemporaryDirectory(directory) as tempdir:
        video_length = draw_frames(frames, tempdir.dir, object_information)
        stitch_video(tempdir.dir, variables.metadata.file_name, video_length, variables.metadata.frame_rate)

    if options.verbose:
        print("Completed generating the video.")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("script_file", help="the file that you would like to compile and generate into a video.")
    parser.add_argument("-v", "--verbose", help="increase output verbosity.", action="store_true")
    parser.add_argument("-d", "--debug", help="adds debug outputs at critical points.", action="store_true")

    args = parser.parse_args()
    try:
        args.script_file = find_path_of_file(args.script_file)
    except FileNotFoundError:
        print(f"FileNotFound: {args.script_file}")
        end_program()

    script_file = args.script_file
    options = Options.from_argparse(args)
    del args  # prevention to calling two variables interchangeably.
    if options.verbose:
        print(f"Started generating the video for '{script_file.name}'.")

    try:
        generate_script(script_file, options)
    except svForceExit:
        end_program()


if __name__ == "__main__":
    main()
