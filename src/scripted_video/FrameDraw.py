from src.scripted_video.variables.ScriptVariables import ScriptVariables

from src.scripted_video.objects.ObjectDict import ObjectDict
from src.scripted_video.objects.frames import Frame

import os
# import shutil
from operator import itemgetter

from PIL import Image

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
            move_time = object_information[objects[0]].get_property("move-time")
            move_rate = object_information[objects[0]].get_property("move-rate")
            for time, rate in zip(move_time, move_rate, strict=True):
                if time <= frame_index < (time + rate):
                    return True


def draw_frames(frames, encoder, object_information: ObjectDict, variables: ScriptVariables):
    frame_rate = variables.metadata.frame_rate

    folder_location = variables.metadata.script_file.parent / encoder
    os.mkdir(folder_location)
    video_length = 0

    for index, frame in enumerate(frames):
        if isinstance(frame, int):
            for _ in range(frame):
                frames[index-1].draw_frame(object_information, folder_location)
            video_length += frame
            continue

        relevant_objects = [object_information[obj] for obj in frame.object]
        for objects in relevant_objects:
            if not objects.moves:
                continue
            move_time = objects.get_property("move-time")
            move_rate = objects.get_property("move-rate")
            for time, rate in zip(move_time, move_rate):
                if time <= frame.index < (time + rate):
                    objects.move_object(frame.index)

        frame.draw_frame(object_information, folder_location)
        video_length += 1

    return folder_location, video_length


'''
def create_video(timetable, object_information, encoder, log_master, traits: ScriptVariables):
    folder_location = traits.metadata.script_file.parent / encoder
    frame_rate = traits.metadata.frame_rate

    os.mkdir(folder_location)

    for index, contents in enumerate(timetable):
        _draw_frames(contents, index, object_information,
                     (traits.metadata.window_width, traits.metadata.window_height),
                     folder_location, encoder)

        if (index + 1) % frame_rate == 0:
            log_master.warning(f"Successfully drew {index+1} frames (equal to {int((index+1)/frame_rate)} seconds).")

    video_length = index
    log_master.warning("Finished drawing the frames for the video.")

    stitch_video(folder_location, traits.metadata.file_name, video_length, frame_rate)

    shutil.rmtree(folder_location)
# '''


'''
def _draw_frames(frame_information, frame_index, object_information, window_dimensions, folder_location, encoder):
    frame = Image.new("RGB", window_dimensions, (255, 255, 255))
    frame_pixel = frame.load()

    for layer, contents in enumerate(frame_information):
        if not contents:
            continue

        if object_information[contents].moves:
            object_information[contents].move_object(frame_index)

        x_home = object_information[contents].x
        y_home = object_information[contents].y

        object_image = Image.open(object_information[contents].file_name)
        object_image_pixel = object_image.load()

        for x in range(x_home, x_home + object_image.width):
            for y in range(y_home, y_home + object_image.height):
                try:
                    frame_pixel.__setitem__((x, y), object_image_pixel.__getitem__((x - x_home, y - y_home)))
                except IndexError:
                    pass

        object_image.close()

    frame.save(f"{folder_location}\\{encoder}__{frame_index}.png", "PNG")
# '''


def stitch_video(folder_location, final_video_name, video_length_frames, frame_rate):
    directory = folder_location.parent
    encoder = folder_location.name

    # clips = [(ImageClip(f"{folder_location}\\{encoder}__{m}.png")
    #           .set_duration(1 / frame_rate))
    #          for m in range(video_length_frames)]
    clips = [(ImageClip(f"{folder_location}\\{m}.png")
              .set_duration(1 / frame_rate))
             for m in range(video_length_frames)]

    concat_clip = concatenate_videoclips(clips, method="compose")
    concat_clip.write_videofile(f"{directory}\\{final_video_name}.mp4", fps=frame_rate)
