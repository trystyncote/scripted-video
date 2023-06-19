from scripted_video.qualms.force_exit import svForceExit
from scripted_video.qualms._root_pseudo_error import PINPOINT_TUPLE, RootPseudoError
from scripted_video.qualms._traceback_functions import write_border_mid, write_border_top, write_cause_line, \
    write_header, write_message, write_pinpoint
from scripted_video.qualms.crash import BaseCrash
from scripted_video.qualms.issues import BaseIssue
from scripted_video.qualms.qualms import BaseQualm


ANY_QUALM_OBJ = BaseIssue | BaseQualm | BaseCrash


class QualmGroup(RootPseudoError):
    __slots__ = ("_qualms",)

    type: str = "group"

    def __init__(self, *qualms: ANY_QUALM_OBJ,
                 cause: str | None = None, file_name: str | None = None, line_number: int | None = None,
                 pinpoint: PINPOINT_TUPLE = None):
        super().__init__(cause=cause, file_name=file_name, line_number=line_number, pinpoint=pinpoint)
        self._qualms = list(qualms)

    @property
    def has_qualms(self):
        return bool(self._qualms)

    def add_qualm(self, added_exception: ANY_QUALM_OBJ):
        self._qualms.append(added_exception)
        if isinstance(added_exception, BaseCrash):
            self.raise_qualms()

    def raise_qualms(self):
        if not self.has_qualms:
            raise ValueError("QualmGroup cannot be raised while empty.")

        if len(self._qualms) == 1:
            self._qualms[0].traceback()
        else:
            self.traceback()

        raise svForceExit

    def traceback(self, *, _series=None):
        if not self._qualms:
            raise UserWarning("QualmGroup has no qualms to write a traceback for.")

        if len(self._qualms) == 1:
            self._qualms[0].traceback()
            return

        _series = [
            write_border_top(37),
            f"| {write_header(self.type, self.__class__.__name__, None, self.file_name)}"
        ]

        for index, qualm in enumerate(self._qualms):
            _series.append(f"{'+-+' if index == 0 else '+'}{write_border_mid(36, index+1)}")
            _series.append(
                f"  | {write_header(qualm.type, qualm.__class__.__name__, qualm.line_number, qualm.file_name)}"
            )  # [3.12] Utilize multi-line behaviour of f-strings to change this line's styling.
            # Default extends too long, against PEP8.
            _series.append(f"  | {write_message(qualm.msg)}")
            if qualm.cause:
                _series.append("  |")
                _series.append(f"  | {write_cause_line(qualm.cause)}")
                if qualm.pinpoint:
                    _series.append(f"  | {write_pinpoint(qualm.pinpoint, len(qualm.cause))}")

        _series.append(f"  | {write_border_top(35)}")
        super().traceback(_series=_series)
