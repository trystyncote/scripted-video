from ._attribute_superclass import SVST_Attribute_Value

from abc import abstractmethod
import re
from typing import Self


class SimpleWhitespace(SVST_Attribute_Value):
    __slots__ = ()  # preventing creation of __dict__.

    @property
    def empty(self):
        return bool(self._value)

    @classmethod
    @abstractmethod
    def evaluate_syntax(cls, match_object: re.Match) -> Self:
        return NotImplemented
