from File import find_path_of_file
from Scripter import Scripter
from Timetable import Timetable


def primary():
    scriptVariable_list = {}
    timetable = []

    xar = Scripter(find_path_of_file("sample_script.txt"))
    yar = None
    yar_collect = ()
    zar = None

    for iar in xar:
        xar.clear_comments()
        xar.find_line_end()

        if xar.linePrevious:
            continue

        yar = xar.define_prefix()

        if yar:
            yar_collect = yar.classify_information()

            if len(yar_collect) == 2:
                scriptVariable_list[yar_collect[0]] = yar_collect[1]

            else:
                timetable.append(yar_collect)

    zar = Timetable(timetable, yar.encoder)


if __name__ == "__main__":
    primary()
