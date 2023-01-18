class Scripter:
    def __init__(self, file: str):
        self.lineCurrent = None
        self.lineNumber = 0
        self._scriptReader = self._read_script(file)
        self.outstandingMultiLine = False

    def __iter__(self):
        return self

    def __next__(self):
        self.lineCurrent = next(self._scriptReader)
        self.lineNumber += 1
        return self.lineCurrent

    def _read_script(self, fileName: str):
        with open(fileName, "r") as fileStore:
            for line in fileStore:
                yield line.rstrip()

    def _clear_line(self, xar: int, yar: int):
        self.lineCurrent = self.lineCurrent[:xar] + self.lineCurrent[yar:]

    def clear_comments(self):
        index = 0
        stringSlice_toCheck = ""

        for iar, var in enumerate(self.lineCurrent):
            stringSlice_toCheck = self.lineCurrent[iar:iar+2]

            if (self.outstandingMultiLine is False
                    and stringSlice_toCheck == "//"):
                self._clear_line(iar, len(self.lineCurrent))

            elif (self.outstandingMultiLine is False
                    and stringSlice_toCheck == "/*"):
                self.outstandingMultiLine = True
                index = iar

            elif (self.outstandingMultiLine is True
                    and stringSlice_toCheck == "*/"):
                self._clear_line(index, iar+2)
                self.outstandingMultiLine = False

        if self.outstandingMultiLine:
            self._clear_line(index, len(self.lineCurrent))
