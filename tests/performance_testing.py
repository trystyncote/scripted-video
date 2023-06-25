from src.scripted_video.utils import find_path_of_file
from src.scripted_video.primary import generate_script

import cProfile
import logging
from pathlib import Path
import pstats


def detect_performance():
    # Code borrowed from mCoding. See the following link:
    # https://github.com/mCodingLLC/VideosSampleCode/blob/master/videos/063_find_why_your_python_code_is_slow_using_this_essential_tool_dot___feat_dot__async_await_/needs_profiling.py
    script = Path(find_path_of_file("svDemo1.txt"))
    logging.basicConfig(format=">> %(message)s")
    logger = logging.getLogger("")

    with cProfile.Profile() as pr:
        generate_script(script, logger)

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
