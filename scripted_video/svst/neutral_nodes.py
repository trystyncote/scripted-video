from ._attribute_superclass import SVST_Attribute_Name, SVST_Attribute_NameValue
from ._dynamic_attributes import dynamic_attributes, SpecificAttribute
from ._functions import gatekeep_indent
from .root_node import SVST_RootNode

from abc import abstractmethod
import re
from typing import Self


@dynamic_attributes
class Doctype(SVST_RootNode):
    __attributes__ = (SpecificAttribute.DOCTYPE,)
    syntax = r"@DOCTYPE [\s| ]*(scripted-video){1}"
    # syntax = r"@DOCTYPE [\s| ]*(scripted-video){1}[\s| ]+((?:TIMELINE)|(?:MASTER[-]*SCRIPT)|(?:DESIGN)){1};"

    @classmethod
    def evaluate_syntax(cls, match_object: re.Match) -> Self:
        doctype = match_object.group(1)
        class_object = cls(doctype)
        return class_object


@dynamic_attributes
class Object(SVST_RootNode):
    """
    The Object node refers to a reference to an object, via the approximate
    syntax [*<object>]. The name of the object is referenced as the 'name'.
    Meant to be referred as a subject of another node.
    """
    __attributes__ = (Attribute.NAME,)



class Property(SVST_Attribute_NameValue):
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
        super().__init__()

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
