from scripted_video.utils import find_path_of_file, Options
from scripted_video.primary import generate_script

import cProfile
from pathlib import Path
import pstats


def detect_performance():
    # Code borrowed from mCoding. See the following link:
    # https://github.com/mCodingLLC/VideosSampleCode/blob/master/videos/063_find_why_your_python_code_is_slow_using_this_essential_tool_dot___feat_dot__async_await_/needs_profiling.py
    script = Path(find_path_of_file("svDemo1.txt"))
    options = Options()
    options.verbose = False

    with cProfile.Profile() as pr:
        generate_script(script, options)

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()


if __name__ == "__main__":
    detect_performance()
