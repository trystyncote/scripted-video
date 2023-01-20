class Compiler:
    def __init__(self, lineCurrent: str, syntax: tuple):
        self.lineData = []
        self._discover_syntax(lineCurrent, syntax)
        self._trim_whitespace()

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

    def _trim_whitespace(self):
        har = 0
        trimmed = False

        while True:
            if self.lineData[har][0] == (" " or "\t"):
                self.lineData[har] = self.lineData[har][1:]
                trimmed = True

            if self.lineData[har][-1] == (" " or "\t"):
                self.lineData[har] = self.lineData[har][:-1]
                trimmed = True

            if trimmed is False:
                har += 1

            if har >= len(self.lineData):
                break

            trimmed = False

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
