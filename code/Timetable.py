class Timetable:
    def __init__(self, fullTimetable: list):
        self.objectInformation = {}
        self.timetableRaw = fullTimetable
        self.timetableSorted = []

        self.objectIndex = {
            "startTime": 1,
            "xCoord": 2,
            "yCoord": 3,
            "scale": 4,
            "layer": 5,
            "moveDetails": 6,
            "deleteTime": 7,
            "delayDelete": 8
        }

        self._collect_information()
        self._define_dimensions()
        self._sort_information()

        for nar, oar in enumerate(self.timetableSorted):
            print(f"{nar}: {oar}")

    def _collect_information(self):
        # "C", objectname, time, x, y, scale, layer
        # "M", objectname, time, x', y', scale', rate
        # "D", objectname, time, delay
        for row in self.timetableRaw:
            if row[0] == "C":
                self.objectInformation[row[1]] = [row[2], row[3], row[4],
                                                  row[5], row[6], row[7], []]

            elif row[0] == "M":
                if row[1] in self.objectInformation is False:
                    # Raise exception for the script.
                    break

                self.objectInformation[row[1]] \
                    [self.objectIndex["moveDetails"]].append([])

                for jar in row[2:]:  # UNSURE: Syntax may not be proper.
                    self.objectInformation[row[1]] \
                        [self.objectIndex["moveDetails"]][-1].append(jar)

            elif row[0] == "D":
                if row[1] in self.objectInformation is False:
                    # Raise exception for the script.
                    break

                for jar in row[2:]:
                    self.objectInformation[row[1]].append(jar)

    def _define_dimensions(self):
        findMax_frame = []
        findMax_layer = []
        for key in self.objectInformation:
            findMax_frame.append(
                self.objectInformation[key][self.objectIndex["startTime"]]
            )
            findMax_frame.append(
                self.objectInformation[key][self.objectIndex["deleteTime"]]
            )
            findMax_layer.append(
                self.objectInformation[key][self.objectIndex["layer"]]
            )

        maxFrame = max(findMax_frame) + 1
        maxLayer = max(findMax_layer)

        for xar in range(maxFrame):
            self.timetableSorted.append([])
            for yar in range(maxLayer):
                self.timetableSorted[xar].append("")

    def _move_details(self, key: str):
        details = []
        for iar in self.objectInformation[key] \
                [self.objectIndex["moveDetails"]]:
            details.append(iar)
        return details
        # changeTime, xChange, yChange, scaleChange, rate
        #        270,     100,     100,         0.0,   15

    def _sort_information(self):
        start = -1
        moveDetails = []
        end = -1
        currentLayer = -1
        moveStart = -1
        moveEnd = -1
        moveStatus = ""

        # row: frame of video
        # col: layer of video
        # thing[x][y] -> x: row, y: col
        for key in self.objectInformation:
            start = self.objectInformation[key][self.objectIndex["startTime"]]
            end = self.objectInformation[key][self.objectIndex["deleteTime"]]
            moveDetails = []
            moveStart = -1
            moveEnd = -1
            moveStatus = ""

            if self.objectInformation[key][self.objectIndex["moveDetails"]]:
                moveDetails = self._move_details(key)
                # moveStart = moveDetails[0]
                # moveEnd = moveStart + moveDetails[4]

            for xar in range(end - start):
                currentLayer = self.objectInformation[key][self.objectIndex["layer"]]
                moveStatus = ()
                for var in moveDetails:
                    moveStart = var[0]
                    moveEnd = moveStart + var[4]
                    if moveStart < (start + xar) <= moveEnd:
                        moveStatus = (var[1], var[2], var[3])
                self.timetableSorted[start+xar][currentLayer-1] = [key, moveStatus]
                # x: self.objectInformation[key][self.objectIndex["xCoord"]]
                # xCoord
