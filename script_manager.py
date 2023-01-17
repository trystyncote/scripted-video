class Scripter:
    def __init__(self, file: str):
        self.lineCurrent = None
        self.lineNumber = None
        self._scriptReader = self._read_script(file)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            self.lineCurrent = next(self._scriptReader)
            self.lineNumber += 1
            return self.lineCurrent
        except StopIteration:
            raise StopIteration

    def _read_script(self, fileName: str):
        with open(fileName, "r") as fileStore:
            for line in fileStore:
                yield line.rstrip()
