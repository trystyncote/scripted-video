class Timetable:
    def __init__(self, fullTimetable: list):
        self.objectInformation = {}
        self.timetableRaw = fullTimetable
        self.timetableSorted = []

        self._collect_information()
        self._define_dimensions()
        self._sort_information()

        for oar in self.timetableSorted:
            print(oar)

    def _collect_information(self):
        # "C", objectname, time, x, y, scale, layer
        # "M", objectname, time, x', y', scale', rate
        # "D", objectname, time, delay
        for row in self.timetableRaw:
            if row[0] == "C":
                self.objectInformation[row[1]] = [row[2], row[3], row[4], row[5], row[6], row[7], []]

            elif row[0] == "M":
                if row[1] in self.objectInformation is False:
                    # Raise exception for the script.
                    break

                self.objectInformation[row[1]][6].append([])

                for jar in row[2:]:  # UNSURE: Syntax may not be proper.
                    self.objectInformation[row[1]][6][-1].append(jar)

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
            findMax_frame.append(self.objectInformation[key][7])
            findMax_frame.append(self.objectInformation[key][1])
            findMax_layer.append(self.objectInformation[key][5])

        maxFrame = max(findMax_frame) + 1
        maxLayer = max(findMax_layer)

        for xar in range(maxFrame):
            self.timetableSorted.append([])
            for yar in range(maxLayer):
                self.timetableSorted[xar].append("")

    def _sort_information(self):
        start = -1
        move = -1
        end = -1

        # row: frame of video
        # col: layer of video
        # thing[x][y] -> x: row, y: col
        for key in self.objectInformation:
            start = self.objectInformation[key][1]
            end = self.objectInformation[key][7]

            if self.objectInformation[key][6]:
                for iar in self.objectInformation[key][6]:
                    # Enters another function to manage how the move information is managed.
                    pass

            for xar, aar in enumerate(self.timetableSorted):
                if xar < start or xar >= end:
                    continue

                for yar, bar in enumerate(aar):
                    if yar + 1 != self.objectInformation[key][5]:
                        continue

                    self.timetableSorted[xar][yar] = [key, ""]  # x, y, scale
