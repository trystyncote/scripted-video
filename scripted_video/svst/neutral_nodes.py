from ._attribute_superclass import _SVST_Attribute_Name, _SVST_Attribute_NameValue
from ._functions import gatekeep_indent
from .root_node import SVST_RootNode

from abc import abstractmethod
import re
from typing import Self


class Doctype(SVST_RootNode):
    __slots__ = ("_doctype",)
    _syntax = r"@DOCTYPE [\s| ]*(scripted-video){1}"
    # _syntax = r"@DOCTYPE [\s| ]*(scripted-video){1}[\s| ]+((?:TIMELINE)|(?:MASTER[-]*SCRIPT)|(?:DESIGN)){1};"

    def __init__(self, doctype: str):
        self._doctype = doctype

    def __repr__(self):
        return f"{self.__class__.__name__}(_doctype={self._doctype})"

    @property
    def doctype(self) -> str:
        return self._doctype

    def convert_to_string(self, *, indent: int = 0, _previous_indent: int = 0) -> str:
        gatekeep_indent(indent)
        return f"{' ' * _previous_indent}{self.__class__.__name__}({self._doctype!r})"

    @classmethod
    def evaluate_syntax(cls, match_object: re.Match) -> Self:
        doctype = match_object.group(1)
        class_object = cls(doctype)
        return class_object

    @classmethod
    def get_syntax(cls):
        # Temporary solution to syntax reading from a neutral node.
        return cls._syntax


class Object(_SVST_Attribute_Name):
    """
    The Object node refers to a reference to an object, via the approximate
    syntax [*<object>]. The name of the object is referenced as the 'name'.
    Meant to be referred as a subject of another node.
    """
    __slots__ = ()

    @classmethod
    @abstractmethod
    def evaluate_syntax(cls, match_object: re.Match) -> Self:
        return NotImplemented


class Property(_SVST_Attribute_NameValue):
    """
    The Property node refers to a call to a property and its value. The name of
    the property is referenced as the 'name', and its value as 'value'. Meant
    to be referred as a member of the body of another node.
    """
    __slots__ = ()

    @classmethod
    @abstractmethod
    def evaluate_syntax(cls, match_object: re.Match) -> Self:
        return NotImplemented


class UnknownSyntax(SVST_RootNode):
    __slots__ = ("_contents",)

    def __init__(self, contents: str):
        self._contents = contents

    def __repr__(self):
        return f"{self.__class__.__name__}(_contents={self._contents!r})"

    @property
    def contents(self):
        return self._contents

    def convert_to_string(self, *, indent: int = 0, _previous_indent: int = 0) -> str:
        gatekeep_indent(indent)
        return f"{' ' * _previous_indent}{self.__class__.__name__}({self._contents!r})"

    @classmethod
    @abstractmethod
    def evaluate_syntax(cls, match_object: re.Match) -> Self:
        return NotImplemented
