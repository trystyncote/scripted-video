from File import find_path_of_file
from Scripter import Scripter


def primary():
    scriptVariable_list = {}

    xar = Scripter(find_path_of_file("sample_script.txt"))
    yar = None
    yar_collect = ()

    for iar in xar:
        xar.clear_comments()
        xar.find_line_end()

        if xar.linePrevious:
            continue

        yar = xar.define_prefix()

        if yar:
            # yar.classify_information()
            yar_collect = yar.classify_information()
            print(yar_collect)


if __name__ == "__main__":
    primary()
