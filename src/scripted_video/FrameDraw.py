from src.scripted_video.variables.ScriptVariables import ScriptVariables

import os
import shutil

from PIL import Image

from moviepy.editor import ImageClip
from moviepy.video.compositing.concatenate import concatenate_videoclips


def create_video(timetable, object_information, encoder, log_master, traits: ScriptVariables):
    folder_location = traits.metadata.script_name.parent / encoder
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

    _stitch_video(folder_location, traits.metadata.file_name, video_length, frame_rate)

    shutil.rmtree(folder_location)


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


def _stitch_video(folder_location, final_video_name, video_length_frames, frame_rate):
    directory = folder_location.parent
    encoder = folder_location.name

    clips = [(ImageClip(f"{folder_location}\\{encoder}__{m}.png")
              .set_duration(1 / frame_rate))
             for m in range(video_length_frames)]

    concat_clip = concatenate_videoclips(clips, method="compose")
    concat_clip.write_videofile(f"{directory}\\{final_video_name}.mp4", fps=frame_rate)
