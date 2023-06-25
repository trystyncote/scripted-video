from src.scripted_video.variables.ScriptVariables import ScriptVariables

from src.scripted_video.objects.ObjectDict import ObjectDict
from src.scripted_video.objects.frames import Frame

from operator import itemgetter

from moviepy.editor import ImageClip
from moviepy.video.compositing.concatenate import concatenate_videoclips


def generate_frames(object_information: ObjectDict, variables: ScriptVariables):
    critical_information = []
    for key, value in object_information.items():
        critical_information.append((key, value.get_property("start-time"), value.get_property("delete-time"), value.moves))
    critical_information = sorted(critical_information, key=itemgetter(1, 2))
    '''
    critical_information contains a series of tuples,
    (object-name, start-time, delete-time, moves)
    Sorted by start-time, ties broken by delete-time.
    '''

    for _, obj in object_information.items():
        obj.open()

    frames_size = (variables.metadata.window_width, variables.metadata.window_height)
    frames = [Frame(0, frames_size)]
    previous_frame: list[tuple[str, int, bool]]
    frame_index = 0
    length = max(max(critical_information, key=itemgetter(1, 2))[1:3])

    while True:
        relevant_objects = []
        for crit_snippet in critical_information:
            if crit_snippet[1] <= frame_index < crit_snippet[2]:
                relevant_objects.append(crit_snippet)

        if frame_index == 0:
            previous_frame = relevant_objects
            for objects in relevant_objects:
                frames[-1].add_object(objects[0])
            frame_index += 1
            continue

        if relevant_objects == previous_frame:
            if _evaluate_move_details(relevant_objects, object_information, frame_index):
                frames.append(Frame(frame_index, frames_size))
                for objects in relevant_objects:
                    frames[-1].add_object(objects[0])
            else:
                if isinstance(frames[-1], int):
                    frames[-1] += 1
                else:
                    frames.append(1)
        else:
            frames.append(Frame(frame_index, frames_size))
            for objects in relevant_objects:
                frames[-1].add_object(objects[0])

        previous_frame = relevant_objects
        frame_index += 1
        if frame_index >= length:
            break

    return frames


def _evaluate_move_details(relevant_objects, object_information, frame_index):
    for objects in relevant_objects:
        if objects[3] is True:
            for adjustment in object_information[objects[0]].adjustments:
                time = adjustment.time
                rate = adjustment.rate
                if time <= frame_index < (time + rate):
                    return True


def draw_frames(frames, directory, object_information: ObjectDict):
    video_length = 0

    for index, frame in enumerate(frames):
        if isinstance(frame, int):
            for _ in range(frame):
                frames[index-1].draw_frame(object_information, directory)
            video_length += frame
            continue

        relevant_objects = [object_information[obj] for obj in frame.object]
        for objects in relevant_objects:
            if not objects.moves:
                continue

            for adjustment in objects.adjustments:
                time = adjustment.time
                rate = adjustment.rate
                if time <= frame.index < (time + rate):
                    objects.move_object(frame.index)

        frame.draw_frame(object_information, directory)
        video_length += 1

    return video_length


def stitch_video(folder_location, final_video_name, video_length_frames, frame_rate):
    directory = folder_location.parent

    clips = [(ImageClip(f"{folder_location}\\{m}.png")
              .set_duration(1 / frame_rate))
             for m in range(video_length_frames)]

    concat_clip = concatenate_videoclips(clips, method="compose")
    concat_clip.write_videofile(f"{directory}\\{final_video_name}.mp4", fps=frame_rate)
