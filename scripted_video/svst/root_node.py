from abc import abstractmethod
import re
from typing import Self


class SVST_RootNode:
    __slots__ = ()  # Defining __slots__ prevents creating of __dict__. It's
    # naturally inherited by subclasses, which is not desired.

    def __init__(self, *args, **kwargs):
        if args:
            raise ValueError(f"{self.__class__.__name__}.__init__ has excess *args: {args}")
        elif kwargs:
            raise ValueError(f"{self.__class__.__name__}.__init__ has excess *kwargs: {kwargs}")

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        return self.convert_to_string()

    @abstractmethod
    def convert_to_string(self, *, indent: int = 0, _previous_indent: int = 0) -> str:
        return NotImplemented

    @classmethod
    @abstractmethod
    def evaluate_syntax(cls, match_object: re.Match) -> Self:
        return NotImplemented
