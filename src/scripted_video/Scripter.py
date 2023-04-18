def _read_script(file_name: str):
    with open(file_name, "r") as file_store:
        for line in file_store:
            yield line.rstrip()


def _clear_line(string: str, start_index: int, end_index: int):
    return string[:start_index] + string[end_index:]


class Scripter:
    def __init__(self, file: str, *, allow_empty_lines: bool = False, allow_rereading: bool = False,
                 auto_clear_comments: bool = False, auto_clear_end_line: bool = False):
        """
        The Scripter class manages a text file and reads it one line at a time,
        which can be iterated over. The syntax of the file is not part of the
        class. The main purpose of the class is to read the script and clear
        the comments and allow multi-line commands.

        :param file: The name of the file containing the script to be run. If
            the file is not available in the same folder as the python script
            file running the class, the file must be provided with the full
            path. Must be in string form.
        :param allow_rereading: OPTIONAL: A boolean for whether the script can
            be read multiple times in different for-loops. If True, then the
            script will allow itself to reread the script when another
            iteration is required. Default is False.
        """
        self._allow_empty_lines = allow_empty_lines  # allow_empty_lines is a
        # flag variable for whether the script should return an empty line when
        # it is asked to iterate. By default, the behaviour prevents the script
        # from returning an empty line.
        self._allow_rereading = allow_rereading  # allow_rereading is a
        # boolean for whether a script can be re-run if the script has already
        # finished running. Note: The Scripter class is unable to tell if the
        # script has been run on a previous running of the full program; it
        # doesn't have a means to tell that. This is merely a preventative
        # measure for accidentally trying to read a script twice.
        self._at_end_of_line = False  # at_end_of_line is a boolean for whether
        # the end-line character has been found. The end-line character is ';'.
        self._auto_clear_comments = auto_clear_comments  # auto_clear_comments
        # is a flag variable for whether the script will automatically call
        # .clear_comments() on each iteration.
        self._auto_clear_end_line = auto_clear_end_line  # auto_clear_end_line
        # is a flag variable for whether the script will automatically call
        # .find_end_line() on each iteration.
        self._file_name = file  # file_name is the name of the text file being
        # read.
        self._finished_reading = False  # finished_reading is for whether the
        # script has been read in full. This variable may become unhelpful if
        # allow_rereading is set to True, where this variable doesn't prevent
        # re-reading.
        self._line_current = None  # line_current refers to the current line of
        # the file being read. Outside the class, it's referred to as
        # 'current_line'.
        self._line_number = 0  # line_number is the number of the line of the
        # file being read. *The variable starts at 1 while the class is being
        # iterated over.*
        self._line_previous = []  # line_previous stores any previous lines
        # that occur without an end-line character at the end. This allows the
        # previous lines to be preserved to allow multi-line commands.
        self._outstanding_multiline_comment = False  # outstanding_multiline...
        # is a boolean that determines if a multi-line comment (/* contents */)
        # is still in effect.
        self._script_reader = None  # script_reader is the variable that stores
        # the generator that iterates over the text file that is being read.

    def __iter__(self):
        self._check_rereading()
        self.reset_script()
        self._script_reader = _read_script(self._file_name)
        return self

    def __next__(self):
        try:
            while True:
                self._line_current = next(self._script_reader)  # line_current is
                # updated by calling next on script_reader, which yields the next line
                # of the text file.

                if self._auto_clear_comments:  # If the flag is set to True, then the
                    self.clear_comments()  # script calls .clear_comments() without the
                    # user being required to call it.
                if self._auto_clear_end_line:  # If the flag is set to True, then the
                    self.find_line_end()  # script calls .find_line_end() without the
                    # user being required to call it.
                    if self._line_previous:
                        continue
                if self._line_current.strip() == "" and not self._allow_empty_lines:
                    continue
                break

        except StopIteration:
            self._finished_reading = True  # The script changes the
            # finished_reading variable to show that the script has been fully
            # read.
            self.reset_script()
            raise StopIteration  # Re-raises the StopIteration exception to
            # allow it to work with a for-loop, as it is intended to be used.

        self._line_number += 1  # Increases line_number by 1.
        return self._line_current  # Only returns line_current because it's the
        # only required variable to return.

    def __index__(self):
        # __index__ is used to allow the enumerate function with the class.
        # Calling enumerate would cause the index (line_number) to be returned.
        return self._line_number

    @property
    def current_line(self):
        """ Get current_line unless the end-line character is not found. """
        # line_current is referred to as current_line externally because it is
        # more clear that way. Internally, line_current is called that because
        # of naming symmetry with other variables (line_number, line_previous).
        if self._line_previous:
            return None

        return self._line_current

    def clear_comments(self, prefix_single_line: str = "//",
                       prefix_multiline: str = "/*",
                       suffix_multiline: str = "*/"):
        """
        clear_comments() goes through the line and looks for any indicator of
        a comment and clears the contents of the line accordingly.

        :param prefix_single_line: The syntax for the single-line comment's
            beginning. Default is '//'.
        :param prefix_multiline: The syntax for the multi-line comment's
            beginning. Default is '/*'.
        :param suffix_multiline:  The syntax for the multi-line comment's end.
            Default is '*/'.
        :return: Has no return.
        """
        if self._line_current == "":
            # There are no comments in an empty line.
            return

        clearing_index = 0  # clearing_index is a variable for holding a value
        # to be for clearing a comment later. This is used for when a multiline
        # comment prefix is found, when it'll hold the value it was at until
        # the suffix is found, if at all.

        for index, _ in enumerate(self._line_current):
            if self._line_current == "":
                # There are no [more?] comments in an empty line.
                return

            if (self._outstanding_multiline_comment is False
                    and (self._line_current[index:index+len(prefix_single_line)]
                         == prefix_single_line)):
                # When the single-line prefix has been found, the rest of the
                # line is the contents of the rest of the comment, so the
                # remainder of the line is cleared.
                self._line_current = _clear_line(self._line_current, index, len(self._line_current))

            elif (self._outstanding_multiline_comment is False
                    and (self._line_current[index:index+len(prefix_multiline)]
                         == prefix_multiline)):
                # When the multi-line prefix has been found, the index variable
                # holds onto the current character's index and sets the
                # outstanding_multiline... variable to True to begin looking
                # for the suffix.
                self._outstanding_multiline_comment = True
                clearing_index = index

            elif (self._outstanding_multiline_comment is True
                    and (self._line_current[index:index+len(suffix_multiline)]
                         == suffix_multiline)):
                # When the multi-line suffix has been found, the line is
                # cleared from the index to the current index, and the search
                # for the suffix is over, so the outstanding_multiline...
                # variable is reset to False.
                self._line_current = _clear_line(self._line_current, clearing_index, index+len(suffix_multiline))
                self._outstanding_multiline_comment = False

        if self._outstanding_multiline_comment:
            # If the multi-line suffix has not yet been found, then the program
            # presumes that it's on a future line, so it clears the remainder
            # of the current line and leaves outstanding_multiline... to True
            # to allow future lines to search for it.
            self._line_current = _clear_line(self._line_current, clearing_index, len(self._line_current))

    def find_line_end(self, syntax_end_line: str = ";"):
        """
        find_line_end() looks for the end-line character and determines if the
        current line has the conclusion to a 'command'. This exists to allow
        multi-line commands to work properly.

        :param syntax_end_line: The character(s) that are used as the end-line
            character(s). Default is ';'.
        :return: Has no return.
        """
        if self._line_current == "":
            # There isn't an end-line character in an empty line.
            return

        for index, _ in enumerate(self._line_current):
            if (self._line_current[index:index+len(syntax_end_line)]
                == syntax_end_line) \
                    and self._at_end_of_line is False:
                # This monstrosity of an if-statement is simply checking for
                # the end-line character when at_end_of_line is False, meaning
                # not found.
                if (self._line_current[index-1] == "\\"
                        and self._line_current[index-2] != "\\"
                        and index > 0):
                    # This statement allows the use of backslashes to prevent
                    # the program misinterpreting a use of it as an end-line
                    # character when not intended.
                    continue

                # The program clears the end-line character from the current
                # line, and set at_end_of_line to True to show it's been found.
                self._line_current = _clear_line(self._line_current, index, index+len(syntax_end_line))
                self._at_end_of_line = True
                break

        # at_end_of_line being False means that the end-line character was not
        # found, meaning the program should add the current line to
        # line_previous to preserve it for when the end-line character *is*
        # found.
        if self._at_end_of_line is False:
            self._line_previous.append(self._line_current)
            return

        # at_end_of_line is reset here because it needs to be reset after it's
        # used, and it is no longer needed.
        self._at_end_of_line = False

        # If there are no previous line to find, then there's no point in
        # adding them to the current line, so there's another early return.
        if not self._line_previous:
            return

        line_combined = ""  # line_combined is used to strap the strings of the
        # previous line and the current one together.
        for index in self._line_previous:
            line_combined += index + " "  # A space is added to prevent any
            # issues with resulting syntax, ie "HEADframe_rate" being incorrect
            # syntax, but not intended.

        # The program then pastes the previous lines, through line_combined, to
        # line_current, and resets line_previous to an empty list.
        self._line_current = line_combined + self._line_current
        self._line_previous = []

    def reset_script(self):
        """
        reset_script() clears the current generator object that the class is
        reading from. If the allow_rereading attribute has been left at False,
        then this function may raise a UserWarning exception.

        :return: Has no return.
        """
        self._script_reader = None  # The class resets the generator object
        # to allow it to make a new generator class if the script wants to
        # read the file a second time without making a new instance of the
        # class.
        self._line_number = 0  # ._line_number is also reset since there is
        # no longer a script to have a line number for.

    def _check_rereading(self):
        if self._finished_reading and not self._allow_rereading:
            raise UserWarning("Scripter has not been allowed to read the script more than once.")
