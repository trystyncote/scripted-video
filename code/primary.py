from File import find_path_of_file, create_encoder
from Scripter import Scripter
from Compiler import define_prefix
from Timetable import Timetable
from FrameDraw import FrameDraw


def primary():
    script_video_traits = {}
    timetable = []

    encoder = create_encoder()

    script = Scripter(find_path_of_file("sample_script.txt"), encoder)
    compile = None
    compile_collect = ()
    timetableClass = None

    for iar in script:
        script.clear_comments()
        script.find_line_end()

        if script.linePrevious:
            continue

        compile = define_prefix(script.current_line, script_video_traits)

        if isinstance(compile, tuple):
            script_video_traits[compile[0]] = compile[1]
            continue

        compile_collect = compile.classify_information()
        timetable.append(compile_collect)

    timetableClass = Timetable(timetable, encoder, script_video_traits)
    frameDrawClass = FrameDraw(timetableClass.timetableSorted,
                               encoder,
                               timetableClass.get_object_names(),
                               script.videoTraits["window_width"],
                               script.videoTraits["window_height"])


if __name__ == "__main__":
    primary()
