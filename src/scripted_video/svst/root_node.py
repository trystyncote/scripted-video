from abc import abstractmethod
from collections.abc import MutableMapping
import re
from typing import Self


class SVST_RootNode:
    __slots__ = ()  # Defining __slots__ prevents creating of __dict__. It's
    # naturally inherited by subclasses, which is not desired.

    syntax_list: MutableMapping = {}

    def __init_subclass__(cls):
        super().__init_subclass__()
        if hasattr(cls, "_syntax"):
            SVST_RootNode.syntax_list[cls] = cls._syntax

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
