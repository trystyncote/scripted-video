from .utils import find_path_of_file, Options
from .primary import generate_script

from .qualms.force_exit import svForceExit

import argparse


def end_program():
    import sys
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("script_file", help="the file that you would like to compile and generate into a video.")
    parser.add_argument("-v", "--verbose", help="increase output verbosity.", action="store_true")
    # currently, the verbose flag is unused. this is a test to allow optional
    # parameters while I work on this feature as the eventual entry point to the
    # program.

    args = parser.parse_args()
    try:
        args.script_file = find_path_of_file(args.script_file)
    except FileNotFoundError:
        print(f"FileNotFound: {args.script_file}")
        end_program()

    options = Options.from_argparse(args)
    print(f">> Started generating the video for '{args.script_file.name}'.")

    try:
        generate_script(args.script_file, options)
    except svForceExit:
        end_program()


if __name__ == "__main__":
    main()
