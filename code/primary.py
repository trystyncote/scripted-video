from File import find_path_of_file
from Scripter import Scripter
from Timetable import Timetable


def primary():
    scriptVariable_list = {}
    timetable = []

    script = Scripter(find_path_of_file("sample_script.txt"))
    compile = None
    compile_collect = ()
    timetableClass = None

    for iar in script:
        script.clear_comments()
        script.find_line_end()

        if script.linePrevious:
            continue

        compile = script.define_prefix()

        if compile:
            compile_collect = compile.classify_information()

            if len(compile_collect) == 2:
                scriptVariable_list[compile_collect[0]] = compile_collect[1]

            else:
                timetable.append(compile_collect)

    timetableClass = Timetable(timetable, compile.encoder)
    print(timetableClass.timetableSorted)


if __name__ == "__main__":
    primary()
