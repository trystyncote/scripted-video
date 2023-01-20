from class_Compile import Compiler, CompileHEAD, CompileSET


class Scripter:
    def __init__(self, file: str):
        self.lineCurrent = None
        self.lineNumber = 0
        self.linePrevious = []
        self._scriptReader = self._read_script(file)
        self._outstandingMultiLine = False
        self._atEnd_ofLine = False

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
        if self.lineCurrent == "":
            return

        index = 0
        stringSlice_toCheck = ""

        for iar, var in enumerate(self.lineCurrent):
            stringSlice_toCheck = self.lineCurrent[iar:iar+2]

            if (self._outstandingMultiLine is False
                    and stringSlice_toCheck == "//"):
                self._clear_line(iar, len(self.lineCurrent))

            elif (self._outstandingMultiLine is False
                    and stringSlice_toCheck == "/*"):
                self._outstandingMultiLine = True
                index = iar

            elif (self._outstandingMultiLine is True
                    and stringSlice_toCheck == "*/"):
                self._clear_line(index, iar+2)
                self._outstandingMultiLine = False

        if self._outstandingMultiLine:
            self._clear_line(index, len(self.lineCurrent))

    def find_line_end(self):
        if self.lineCurrent == "":
            return

        for iar, var in enumerate(self.lineCurrent):
            if var == ";" and self._atEnd_ofLine is False:
                if (self.lineCurrent[iar-1] == "\\"
                        and self.lineCurrent[iar-2] != "\\"
                        and iar > 0):
                    continue

                self._clear_line(iar, iar+1)
                self._atEnd_ofLine = True

        if self._atEnd_ofLine is False:
            self.linePrevious.append(self.lineCurrent)
            return

        self._atEnd_ofLine = False

        if not self.linePrevious:
            return

        lineCombined = ""
        for iar in self.linePrevious:
            lineCombined += iar + " "

        self.lineCurrent = lineCombined + self.lineCurrent
        self.linePrevious = []

    def define_prefix(self):
        if self.lineCurrent[0:5].upper() == "HEAD ":
            return CompileHEAD(self.lineCurrent)

        elif self.lineCurrent[0:4].upper() == "SET ":
            return CompileSET(self.lineCurrent)

        return None
