from File import find_path_of_file
import os
from PIL import Image


class FrameDraw:
    def __init__(self, timetable: list, encoder: str, objectFiles: dict,
                 windowWidth: int, windowHeight: int,
                 folderLocation = find_path_of_file("sample_script.txt").rpartition("\\")):
        self.encoder = encoder
        self.timetable = timetable
        self.objectFiles = objectFiles
        self.windowDimensions = (windowWidth, windowHeight)

        os.mkdir(f"{folderLocation[0]}\\{self.encoder}")
        self.folderLocation = f"{folderLocation[0]}\\{self.encoder}"

        for index, contents in enumerate(self.timetable):
            self.draw_frame(index)

    def draw_frame(self, index: int):
        frame = Image.new("RGB", self.windowDimensions, (255, 255, 255))
        framePixel = frame.load()

        for layer, contents in enumerate(self.timetable[index]):
            if not contents:
                continue

            xHome = self.timetable[index][1]
            yHome = self.timetable[index][2]

            objectImage = Image.open(self.objectFiles[self.timetable[index][layer][0]])
            objectImage_pixel = objectImage.load()

            for i in range(xHome, objectImage.width):
                for j in range(yHome, objectImage.height):
                    framePixel.__setitem__((i, j), objectImage_pixel.__getitem__((i, j)))

            objectImage.close()

        frame.save(self.folderLocation + "\\" + self.encoder + "__" + index, "PNG")
