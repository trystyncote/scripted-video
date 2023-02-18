import os
import shutil

from PIL import Image

from moviepy.editor import ImageClip
from moviepy.video.compositing.concatenate import concatenate_videoclips


def create_video(timetable, object_information, encoder, l, **traits):
    script_path = traits["_script_name"].rpartition("\\")[0]
    folder_location = f"{script_path}\\{encoder}"
    frame_rate = traits["frame_rate"]

    os.mkdir(folder_location)

    for index, contents in enumerate(timetable):
        _draw_frames(contents, index, object_information, (traits["window_width"], traits["window_height"]),
                     folder_location, encoder)

        if (index + 1) % frame_rate == 0:
            l.warning(f"Successfully drew {index+1} frames (equal to {int((index+1)/frame_rate)} seconds).")

    video_length = index
    l.warning("Finished drawing the frames for the video.")

    _stitch_video(folder_location, traits["file_name"], video_length, traits["frame_rate"])

    shutil.rmtree(folder_location)


def _draw_frames(frame_information, frame_index, object_information, window_dimensions, folder_location, encoder):
    frame = Image.new("RGB", window_dimensions, (255, 255, 255))
    frame_pixel = frame.load()
    x_alter = 0
    y_alter = 0
    scale_alter = 0.0

    for layer, contents in enumerate(frame_information):
        if not contents:
            continue

        if object_information[contents].moves:
            object_information[contents].move_object(frame_index)
            # x_alter, y_alter, scale_alter = _collect_move_details(frame_index, contents, object_information)

        x_home = object_information[contents].x + x_alter
        y_home = object_information[contents].y + y_alter

        object_image = Image.open(object_information[contents].file_name)
        object_image_pixel = object_image.load()

        for x in range(x_home, x_home + object_image.width):
            for y in range(y_home, y_home + object_image.height):
                frame_pixel.__setitem__((x, y), object_image_pixel.__getitem__((x - x_home, y - y_home)))

        object_image.close()

    frame.save(f"{folder_location}\\{encoder}__{frame_index}.png", "PNG")


def _collect_move_details(frame_index, object_index, object_information):
    x_alter = 0
    y_alter = 0
    scale_alter = 0.0
    frame_difference = -1

    for time, x, y, scale, rate in object_information[object_index]:
        if frame_index > time:
            frame_difference = (frame_index - time + 1)
            if frame_index < time + rate:
                frame_difference -= (frame_index - (time + rate))
            x_alter += int(frame_difference * (x / rate))
            y_alter += int(frame_difference * (y / rate))
            scale_alter += int(frame_difference * (scale / rate))

    return x_alter, y_alter, scale_alter


def _stitch_video(folder_location, final_video_name, video_length_frames, frame_rate):
    directory, encoder = folder_location.rsplit("\\", 1)
    clips = [(ImageClip(f"{folder_location}\\{encoder}__{m}.png")
              .set_duration(1 / frame_rate))
             for m in range(video_length_frames)]

    concat_clip = concatenate_videoclips(clips, method="compose")
    concat_clip.write_videofile(f"{directory}\\{final_video_name}.mp4", fps=frame_rate)


'''
def stitch_video(input_folder_location, output_final_video_name: str, video_length_frames: int, frame_rate: int = 24):
    directory, encoder = input_folder_location.rsplit("\\", 1)
    clips = [(ImageClip(f"{input_folder_location}\\{encoder}__{m}.png")
              .set_duration(1 / frame_rate))
             for m in range(video_length_frames)]

    concat_clip = concatenate_videoclips(clips, method="compose")
    concat_clip.write_videofile(f"{directory}\\{output_final_video_name}.mp4",
                                fps=frame_rate)
'''
'''
class FrameDraw:
    def __init__(self, timetable: list, encoder: str, objectFiles: dict,
                 windowWidth: int, windowHeight: int,
                 folderLocation=find_path_of_file("sample_script.txt").rpartition("\\")):
        self.encoder = encoder
        self.timetable = timetable
        self.objectFiles = objectFiles
        self.windowDimensions = (windowWidth, windowHeight)
        self.folderLocation = f"{folderLocation[0]}\\{self.encoder}"

        os.mkdir(f"{folderLocation[0]}\\{self.encoder}")

        for index, contents in enumerate(self.timetable):
            self.draw_frame(index)
        self._video_length_frames = index

        # Manual declaration of variables is temporary.
        stitch_video(self.folderLocation, "final", self._video_length_frames, 30)

        shutil.rmtree(self.folderLocation)
'''
'''
    def draw_frame(self, index: int):
        frame = Image.new("RGB", self.windowDimensions, (255, 255, 255))
        framePixel = frame.load()

        for layer, contents in enumerate(self.timetable[index]):
            if not contents:
                continue

            xHome = int(self.timetable[index][layer][1])
            yHome = int(self.timetable[index][layer][2])

            objectImage = Image.open(self.objectFiles[self.timetable[index][layer][0]])
            objectImage_pixel = objectImage.load()

            for i in range(xHome, xHome + objectImage.width):
                for j in range(yHome, yHome + objectImage.height):
                    framePixel.__setitem__((i, j), objectImage_pixel.__getitem__((i - xHome, j - yHome)))

            objectImage.close()

        frame.save(f"{self.folderLocation}\\{self.encoder}__{index}.png", "PNG")

    @property
    def video_length_frames(self):
        return self._video_length_frames
'''
