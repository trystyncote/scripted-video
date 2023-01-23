class Compiler:
    def __init__(self, lineCurrent: str, syntax: tuple):
        self.lineData = []
        self._discover_syntax(lineCurrent, syntax)

        for iar, var in enumerate(self.lineData):
            self.lineData[iar] = var.strip()

    def _discover_syntax(self, lineCurrent: str, syntax: tuple):
        outstandingParenthesis = False  # ()
        outstandingBrackets = False  # []
        outstandingBraces = False  # {}
        outstandingSingle_quotes = False  # ''
        outstandingDouble_quotes = False  # ""

        syntaxIndex = 0
        har = 0

        for iar, var in enumerate(lineCurrent):
            if not outstandingParenthesis and var == "(":
                outstandingParenthesis = True
                continue
            elif outstandingParenthesis and var == ")":
                outstandingParenthesis = False
                continue

            if not outstandingBrackets and var == "[":
                outstandingBrackets = True
                continue
            elif outstandingBrackets and var == "]":
                outstandingBrackets = False
                continue

            if not outstandingBraces and var == "{":
                outstandingBraces = True
                continue
            elif outstandingBraces and var == "}":
                outstandingBraces = False
                continue

            if not outstandingSingle_quotes and var == "'":
                outstandingSingle_quotes = True
                continue
            elif outstandingSingle_quotes:
                if var == "'":
                    outstandingSingle_quotes = False
                continue

            if not outstandingDouble_quotes and var == '"':
                outstandingDouble_quotes = True
                continue
            elif outstandingDouble_quotes:
                if var == '"':
                    outstandingDouble_quotes = False
                continue

            # Find members of syntax...
            '''
            if type() == tuple:
                for jar in syntax[har]:
            '''
            if lineCurrent[iar:iar+len(syntax[har])].upper() == syntax[har]:
                if har != 0:
                    self.lineData.append(lineCurrent[syntaxIndex:iar])
                syntaxIndex = iar + len(syntax[har])
                self.lineData.append(lineCurrent[iar:iar+len(syntax[har])])
                # lineCurrent = lineCurrent[iar+len(syntax[har]):]

                while True:
                    har += 1
                    try:
                        if syntax[har][0] != "@":
                            break
                    except IndexError:
                        break

            try:
                syntax[har]
            except IndexError:
                self.lineData.append(lineCurrent[iar+1:])
                break

            if iar >= len(lineCurrent):
                break

    def classify_information(self):
        # To be overridden by child classes.
        pass


class CompileHEAD(Compiler):
    syntax = ("HEAD ", "@variable", "=", "@value")

    def __init__(self, lineCurrent: str):
        super().__init__(lineCurrent, self.syntax)

    def classify_information(self):
        keywordList = ["window_width", "window_height", "frame_rate",
                       "file_name"]
        identifyVariable = self.lineData[1]
        identifyValue = self.lineData[3]

        for iar in keywordList:
            if iar == identifyVariable:
                return identifyVariable, identifyValue

        # Raise exception for the script.
        return None


class CompileSET(Compiler):
    syntax = ("SET ", "@variable", "=", "@value", " AS ", "@type")

    def __init__(self, lineCurrent: str):
        super().__init__(lineCurrent, self.syntax)

    def classify_information(self):
        identifyVariable = self.lineData[1]
        identifyValue = self.lineData[3]
        identifyType = self.lineData[5]

        if identifyType.upper() == "INT":
            identifyValue = int(identifyValue)

        elif identifyType.upper() == "FLOAT":
            identifyValue = float(identifyValue)

        elif identifyType.upper() == "BOOL":
            identifyValue = bool(identifyValue)

        elif identifyType.upper() == "STRING":
            pass

        elif identifyType.upper() == "ADDRESS":
            # Collect directory.
            pass

        else:
            # Raise exception for the script.
            pass

        return identifyVariable, identifyValue


class CompileOBJECT(Compiler):
    syntaxCreate = ("CREATE OBJECT <", "@filename", ">", ":",
                    "@initialtime", ",", "@x", ",", "@y", ",", "@scale", ",",
                    "@layer")
    syntaxMove = ("MOVE OBJECT <", "@filename", ">", ":",
                  "@changetime", ",", "@xchange", ",", "@ychange", ",",
                  "@scale", ",", "@rate")
    syntaxDelete = ("DELETE OBJECT <", "@filename", ">", ":",
                    "@deletetime", ",", "@delay")

    def __init__(self, lineCurrent: str, **kwargs):
        index = lineCurrent.find(" ", 4)
        self.classification = lineCurrent[:index].strip()

        if self.classification == "CREATE":
            super().__init__(lineCurrent, self.syntaxCreate)
        elif self.classification == "MOVE":
            super().__init__(lineCurrent, self.syntaxMove)
        elif self.classification == "DELETE":
            super().__init__(lineCurrent, self.syntaxDelete)
        else:
            # Raise exception for the script.
            pass

        self._kwargs = {}
        for key, value in kwargs.items():
            self._kwargs[key] = value

    def _manage_time(self, stringToDissect: str):
        frame_rate = self._kwargs["frame_rate"]
        stringToDissect = (stringToDissect + " ").split(" ")
        _ = stringToDissect.pop(-1)
        suffixEffect = {"f": 1, "s": frame_rate, "m": frame_rate*60,
                        "h": frame_rate*60*60}

        aar = 0.0
        for iar in stringToDissect:
            aar += float(iar[:-1]) * suffixEffect[iar[-1]]

        return aar

    def _create(self):
        identifyInitialTime = self._manage_time(self.lineData[5])
        identifyX = int(self.lineData[7])
        identifyY = int(self.lineData[9])
        identifyScale = float(self.lineData[11])
        identifyLayer = int(self.lineData[13])

        return identifyInitialTime, identifyX, identifyY, identifyScale, \
            identifyLayer

    def _move(self):
        identifyChangeTime = self._manage_time(self.lineData[5])
        identifyXChange = int(self.lineData[7])
        identifyYChange = int(self.lineData[9])
        identifyScaleChange = float(self.lineData[11])
        identifyRate = self._manage_time(self.lineData[13])

        return identifyChangeTime, identifyXChange, identifyYChange, \
            identifyScaleChange, identifyRate

    def _delete(self):
        identifyDeleteTime = self._manage_time(self.lineData[5])
        identifyDelay = self.lineData[7]

        return identifyDeleteTime, identifyDelay

    def classify_information(self):
        if self.classification == "CREATE":
            return self._create()

        elif self.classification == "MOVE":
            return self._move()

        elif self.classification == "DELETE":
            return self._delete()

        return None
