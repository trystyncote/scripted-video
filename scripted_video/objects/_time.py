from typing import TypeVar


TIME = TypeVar("TIME")


def _manage_time(time_string: str, frame_rate: int):
    try:
        time_string = int(time_string)
    except ValueError:
        pass
    else:
        return time_string

    time_string_list = (time_string + " ").split(" ")  # time_string splits itself
    # by the whitespace because the full command must be split that way by
    # default. Example: "2s 15f" refers to 2 seconds, and 15 frames after that.
    _ = time_string_list.pop(-1)
    # f: frame, s: seconds, m: minutes, h: hours
    suffix_effect = {"f": 1,
                     "s": frame_rate,  # The amount of frames per second is a
                     "m": frame_rate * 60,  # variable amount, so it's manually
                     "h": frame_rate * 60 * 60}  # calculated here.

    time = 0.0  # This variable is to store the amount of frames per unit as
    # it is iterated over.
    for i in time_string_list:
        try:
            time += float(i[:-1]) * suffix_effect[i[-1]]  # The float member of
            # the number 'i[:-1]', meaning before the suffix, is multiplied by
            # the suffix effect denoted by the specific character.
        except KeyError:
            time += float(i)

    return int(time)
