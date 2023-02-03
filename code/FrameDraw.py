from File import find_path_of_file

from PIL import Image
import os
import shutil

from moviepy.editor import ImageClip
from moviepy.video.compositing.concatenate import concatenate_videoclips


def stitch_video(input_folder_location, output_final_video_name: str, video_length_frames: int, frame_rate: int = 24):
    directory, encoder = input_folder_location.rsplit("\\", 1)
    clips = [(ImageClip(f"{input_folder_location}\\{encoder}__{m}.png")
              .set_duration(1 / frame_rate))
             for m in range(video_length_frames)]

    concat_clip = concatenate_videoclips(clips, method="compose")
    concat_clip.write_videofile(f"{directory}\\{output_final_video_name}.mp4",
                                fps=frame_rate)


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
