from .force_exit import svForceExit
from ._traceback_functions import write_cause_line, write_header, write_message, write_pinpoint

from logging import Formatter as loggingFormatter, StreamHandler as loggingHandler, getLogger


PINPOINT_TUPLE = tuple[tuple[int, int], tuple[int, int]] | tuple[int, int] | None
# This is an unreadable type hinting variable for the following cases:
# ((a, b), (c, d)) or (a, b); where a, b, c, and d are integers that represent
# indexes of the error message. This is also an optional parameter.


class RootPseudoError:
    __slots__ = ("cause", "file_name", "line_number", "pinpoint")

    msg: str = ""
    type: str = ""

    def __init__(self, *,
                 cause: str | None = None, file_name: str | None = None, line_number: int | None = None,
                 pinpoint: PINPOINT_TUPLE = None):
        self.cause = cause
        self.file_name = file_name
        self.line_number = line_number
        self.pinpoint = pinpoint  # _pinpoint is the identity of any arrow
        # display to be printed in the traceback. (ie ^^^)

    def raise_qualms(self):
        self.traceback()
        raise svForceExit

    def traceback(self, *, _series=None):
        # :type: NameOfQualm
        #   Error message.
        #
        # SOME COMMAND
        #      ^^^^^^^

        handler = loggingHandler()
        handler.setFormatter(loggingFormatter("%(message)s"))
        logger = getLogger("QUALM_LOGGER")
        logger.propagate = False
        logger.handlers.clear()
        logger.addHandler(handler)

        if _series is None:
            _series = [
                write_header(self.type, self.__class__.__name__, self.line_number, self.file_name),
                write_message(self.msg)
            ]
            if self.cause:
                _series.append("")
                _series.append(write_cause_line(self.cause))
                if self.pinpoint:
                    _series.append(write_pinpoint(self.pinpoint, len(self.cause)))

        for string in _series:
            logger.log(50, string)
