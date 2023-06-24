from ._functions import create_string_from_sequence, define_indent_sequence, gatekeep_indent
from .root_node import SVST_RootNode

from abc import abstractmethod
from collections.abc import MutableSequence
import re
from typing import Self


class _SVST_Attribute_Body(SVST_RootNode):
    __slots__ = ("_body",)

    def __init__(self):
        self._body = []

    def __repr__(self):
        return f"{self.__class__.__name__}(_body={[node.__class__.__name__ for node in self._body]})"

    @property
    def body(self) -> MutableSequence:
        return self._body

    def convert_to_string(self, *, indent: int = 0, _previous_indent: int = 0) -> str:
        gatekeep_indent(indent)
        if len(self._body) == 0:
            return f"{' ' * _previous_indent}{self.__class__.__name__}(body=[])"

        indent_sequence = define_indent_sequence(indent, _previous_indent)
        return (
            f"{' ' * _previous_indent}{self.__class__.__name__}("
            + create_string_from_sequence(self._body, "body", indent, indent+_previous_indent)
            + f"{indent_sequence})"
        )

    @classmethod
    @abstractmethod
    def evaluate_syntax(cls, match_object: re.Match) -> Self:
        return NotImplemented


class _SVST_Attribute_Subjects(SVST_RootNode):
    __slots__ = ("_subjects",)

    def __init__(self):
        self._subjects = []

    def __repr__(self):
        return f"{self.__class__.__name__}(_subjects={[node.__class__.__name__ for node in self._subjects]})"

    @property
    def subjects(self) -> MutableSequence:
        return self._subjects

    def convert_to_string(self, *, indent: int = 0, _previous_indent: int = 0) -> str:
        gatekeep_indent(indent)
        if len(self._subjects) == 0:
            return f"{' ' * _previous_indent}{self.__class__.__name__}(subjects=[])"

        indent_sequence = define_indent_sequence(indent, _previous_indent)
        return (
            f"{' ' * _previous_indent}{self.__class__.__name__}("
            + create_string_from_sequence(self._subjects, "subjects", indent, indent+_previous_indent)
            + f"{indent_sequence})"
        )

    @classmethod
    @abstractmethod
    def evaluate_syntax(cls, match_object: re.Match) -> Self:
        return NotImplemented


class _SVST_Attribute_BodySubjects(SVST_RootNode):
    __slots__ = ("_body", "_subjects")

    def __init__(self):
        self._body = []
        self._subjects = []

    def __repr__(self):
        return f"{self.__class__.__name__}(_body={[node.__class__.__name__ for node in self._body]}, " \
               f"_subjects={[node.__class__.__name__ for node in self._subjects]})"

    @property
    def body(self) -> MutableSequence:
        return self._body

    @property
    def subjects(self) -> MutableSequence:
        return self._subjects

    def convert_to_string(self, *, indent: int = 0, _previous_indent: int = 0) -> str:
        gatekeep_indent(indent)
        indent_sequence = define_indent_sequence(indent, _previous_indent)
        return (
            f"{' ' * _previous_indent}{self.__class__.__name__}("
            + create_string_from_sequence(self._body, "body", indent, indent+_previous_indent)
            + ", "
            + create_string_from_sequence(self._subjects, "subjects", indent, indent+_previous_indent)
            + f"{indent_sequence})"
        )

    @classmethod
    @abstractmethod
    def evaluate_syntax(cls, match_object: re.Match) -> Self:
        return NotImplemented


class _SVST_Attribute_Name(SVST_RootNode):
    __slots__ = ("_name",)

    def __init__(self, name: str):
        self._name = name

    def __repr__(self):
        return f"{self.__class__.__name__}(_name={self._name})"

    @property
    def name(self) -> str:
        return self._name

    def convert_to_string(self, *, indent: int = 0, _previous_indent: int = 0) -> str:
        gatekeep_indent(indent)
        return f"{' ' * _previous_indent}{self.__class__.__name__}(name={self._name!r})"

    @classmethod
    @abstractmethod
    def evaluate_syntax(cls, match_object: re.Match) -> Self:
        return NotImplemented


class _SVST_Attribute_NameValue(SVST_RootNode):
    __slots__ = ("_name", "_value")

    def __init__(self, name: str, value: str):
        self._name = name
        self._value = value

    def __repr__(self):
        return f"{self.__class__.__name__}(_name={self._name}, _value={self._value})"

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> str:
        return self._value

    def convert_to_string(self, *, indent: int = 0, _previous_indent: int = 0) -> str:
        gatekeep_indent(indent)
        indent_sequence = define_indent_sequence(indent, _previous_indent)
        return (
            f"{indent_sequence[1:]}{self.__class__.__name__}("
            f"{indent_sequence}{' ' * indent}name={self._name!r}, "
            f"{indent_sequence}{' ' * indent}value={self._value!r}"
            f"{indent_sequence})"
        )

    @classmethod
    @abstractmethod
    def evaluate_syntax(cls, match_object: re.Match) -> Self:
        return NotImplemented
