from Scripter import Scripter
from Compiler import Compiler, CompileHEAD, CompileSET
import os


def find_path_of_file(desiredFile_name: str, absoluteTop: str = "C:\\"):
    for root, dirs, files in os.walk(absoluteTop):
        for name in files:
            if name == desiredFile_name:
                return os.path.abspath(os.path.join(root, name))


def primary():
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
