from .File import find_path_of_file
from .primary import generate_script

import argparse
import logging


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
        import sys
        sys.exit(1)

    logging.basicConfig(format=">> %(message)s")
    logger = logging.getLogger("")

    generate_script(args.script_file, logger)


if __name__ == "__main__":
    main()
