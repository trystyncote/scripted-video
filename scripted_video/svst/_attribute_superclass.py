from ._functions import create_string_from_sequence, define_indent_sequence, gatekeep_indent
from .root_node import SVST_RootNode

from abc import abstractmethod
from collections.abc import MutableSequence
import re
from typing import Self


def _factory_Attribute_Body(class_name: str, /, *, inherited_classes: type[object] = object):
    class FACTORY(inherited_classes):
        __slots__ = ("_body",)

        def __init__(self, *args, **kwargs):
            self._body = []
            super().__init__(*args, **kwargs)

        def __repr__(self):
            return f"{self.__class__.__name__}(_body={[node.__class__.__name__ for node in self._body]})"

        @property
        def body(self) -> MutableSequence:
            return self._body

        def convert_to_string(self, *, indent: int = 0, _previous_indent: int = 0) -> str:
            gatekeep_indent(indent)
            if len(self._body) == 0:
                return f"{' ' * _previous_indent}{self.__class__.__name__}(body=[])"

            return (
                    f"{' ' * _previous_indent}{self.__class__.__name__}("
                    + create_string_from_sequence(self._body, "body", indent, indent + _previous_indent)
                    + ")"
            )

        @classmethod
        @abstractmethod
        def evaluate_syntax(cls, match_object: re.Match) -> Self:
            return NotImplemented

    FACTORY.__name__ = class_name
    FACTORY.__qualname__ = class_name
    return FACTORY


def _factory_Attribute_Subjects_plural(class_name: str, /, *, inherited_classes: type[object] = object):
    class FACTORY(inherited_classes):
        __slots__ = ("_subjects",)

        def __init__(self, *args, **kwargs):
            self._subjects = []
            super().__init__(*args, **kwargs)

        def __repr__(self):
            return f"{self.__class__.__name__}(_subjects={[node.__class__.__name__ for node in self._subjects]})"

        @property
        def subjects(self) -> MutableSequence:
            return self._subjects

        def convert_to_string(self, *, indent: int = 0, _previous_indent: int = 0) -> str:
            gatekeep_indent(indent)
            if len(self._subjects) == 0:
                return f"{' ' * _previous_indent}{self.__class__.__name__}(subjects=[])"

            return (
                    f"{' ' * _previous_indent}{self.__class__.__name__}("
                    + create_string_from_sequence(self._subjects, "subjects", indent, indent + _previous_indent)
                    + ")"
            )

        @classmethod
        @abstractmethod
        def evaluate_syntax(cls, match_object: re.Match) -> Self:
            return NotImplemented

    FACTORY.__name__ = class_name
    FACTORY.__qualname__ = class_name
    return FACTORY


def _factory_Attribute_Name(class_name: str, /, *, inherited_classes: type[object] = object):
    class FACTORY(inherited_classes):
        __slots__ = ("_name",)

        def __init__(self, name: str, *args, **kwargs):
            self._name = name
            super().__init__(*args, **kwargs)

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

    FACTORY.__name__ = class_name
    FACTORY.__qualname__ = class_name
    return FACTORY


def _factory_Attribute_Value(class_name: str, /, *, inherited_classes: type[object] = object):
    class FACTORY(inherited_classes):
        __slots__ = ("_value",)

        def __init__(self, value: str, *args, **kwargs):
            self._value = value
            super().__init__(*args, **kwargs)

        def __repr__(self):
            return f"{self.__class__.__name__}(_value={self._value})"

        @property
        def value(self) -> str:
            return self._value

        def convert_to_string(self, *, indent: int = 0, _previous_indent: int = 0) -> str:
            gatekeep_indent(indent)
            indent_sequence = define_indent_sequence(indent, _previous_indent)
            return f"{indent_sequence[1:]}{self.__class__.__name__}(value={self._value!r})"

        @classmethod
        @abstractmethod
        def evaluate_syntax(cls, match_object: re.Match) -> Self:
            return NotImplemented

    FACTORY.__name__ = class_name
    FACTORY.__qualname__ = class_name
    return FACTORY


def _factory_Attribute_WhitespaceAfterEqualSign(class_name: str, /, *, inherited_classes: type[object] = object):
    class FACTORY(inherited_classes):
        __slots__ = ("whitespace_after_equal_sign",)

        def __init__(self, ws_after_equal: str = "", *args, **kwargs):
            self.whitespace_after_equal_sign = ws_after_equal
            super().__init__(*args, **kwargs)

        def __repr__(self):
            if not hasattr(self, "whitespace_after_equal_sign"):
                return f"{self.__class__.__name__}()"
            else:
                return f"{self.__class__.__name__}(whitespace_after_equal_sign={self.whitespace_after_equal_sign})"

        def convert_to_string(self, *, indent: int = 0, _previous_indent: int = 0) -> str:
            gatekeep_indent(indent)
            return (
                f"{' ' * _previous_indent}{self.__class__.__name__}("
                f"whitespace_after_keyword={self.whitespace_after_equal_sign})"
            )

        @classmethod
        @abstractmethod
        def evaluate_syntax(cls, match_object: re.Match) -> Self:
            return NotImplemented

    FACTORY.__name__ = class_name
    FACTORY.__qualname__ = class_name
    return FACTORY


def _factory_Attribute_WhitespaceAfterKeyword(class_name: str, /, *, inherited_classes: type[object] = object):
    class FACTORY(inherited_classes):
        __slots__ = ("whitespace_after_keyword",)

        def __init__(self, ws_after_keyword: str = "", *args, **kwargs):
            self.whitespace_after_keyword = ws_after_keyword
            super().__init__(*args, **kwargs)

        def __repr__(self):
            if not hasattr(self, "whitespace_after_keyword"):
                return f"{self.__class__.__name__}()"
            else:
                return f"{self.__class__.__name__}(whitespace_after_keyword={self.whitespace_after_keyword})"

        def convert_to_string(self, *, indent: int = 0, _previous_indent: int = 0) -> str:
            gatekeep_indent(indent)
            return (
                f"{' ' * _previous_indent}{self.__class__.__name__}("
                f"whitespace_after_keyword={self.whitespace_after_keyword})"
            )

        @classmethod
        @abstractmethod
        def evaluate_syntax(cls, match_object: re.Match) -> Self:
            return NotImplemented

    FACTORY.__name__ = class_name
    FACTORY.__qualname__ = class_name
    return FACTORY


def _factory_Attribute_WhitespaceBeforeEqualSign(class_name: str, /, *, inherited_classes: type[object] = object):
    class FACTORY(inherited_classes):
        __slots__ = ("whitespace_before_equal_sign",)

        def __init__(self, ws_before_equal: str = "", *args, **kwargs):
            self.whitespace_before_equal_sign = ws_before_equal
            super().__init__(*args, **kwargs)

        def __repr__(self):
            if not hasattr(self, "whitespace_before_equal_sign"):
                return f"{self.__class__.__name__}()"
            else:
                return f"{self.__class__.__name__}(whitespace_before_equal_sign={self.whitespace_before_equal_sign})"

        def convert_to_string(self, *, indent: int = 0, _previous_indent: int = 0) -> str:
            gatekeep_indent(indent)
            return (
                f"{' ' * _previous_indent}{self.__class__.__name__}("
                f"whitespace_after_keyword={self.whitespace_before_equal_sign})"
            )

        @classmethod
        @abstractmethod
        def evaluate_syntax(cls, match_object: re.Match) -> Self:
            return NotImplemented

    FACTORY.__name__ = class_name
    FACTORY.__qualname__ = class_name
    return FACTORY


_SVST_Attribute_Body = _factory_Attribute_Body("_SVST_Attribute_Body", inherited_classes=SVST_RootNode)
_SVST_Attribute_Subjects = _factory_Attribute_Subjects_plural("_SVST_Attribute_Subjects",
                                                              inherited_classes=SVST_RootNode)
_SVST_Attribute_BodySubjects = _factory_Attribute_Subjects_plural("_SVST_Attribute_BodySubjects",
                                                                  inherited_classes=_SVST_Attribute_Body)
_SVST_Attribute_Name = _factory_Attribute_Name("_SVST_Attribute_Name", inherited_classes=SVST_RootNode)
_SVST_Attribute_Value = _factory_Attribute_Value("_SVST_Attribute_Value", inherited_classes=SVST_RootNode)
_SVST_Attribute_NameValue = _factory_Attribute_Value("_SVST_Attribute_NameValue",
                                                     inherited_classes=_SVST_Attribute_Name)


def _redefined_combo_Attribute_BodySubjects():
    def redefined_repr(self):
        return f"{self.__class__.__name__}(_body={[node.__class__.__name__ for node in self._body]}, " \
               f"_subjects={[node.__class__.__name__ for node in self._subjects]})"

    def convert_to_string(self, *, indent: int = 0, _previous_indent: int = 0) -> str:
        gatekeep_indent(indent)
        return (
                f"{' ' * _previous_indent}{self.__class__.__name__}("
                + create_string_from_sequence(self._body, "body", indent, indent + _previous_indent)
                + ", "
                + create_string_from_sequence(self._subjects, "subjects", indent, indent + _previous_indent)
                + ")"
        )

    return redefined_repr, convert_to_string


_SVST_Attribute_BodySubjects.__repr__, \
    _SVST_Attribute_BodySubjects.convert_to_string = _redefined_combo_Attribute_BodySubjects()


def _redefined_combo_Attribute_NameValue():
    def redefined_repr(self):
        return f"{self.__class__.__name__}(_name={self._name}, _value={self._value})"

    def convert_to_string(self, *, indent: int = 0, _previous_indent: int = 0) -> str:
        gatekeep_indent(indent)
        indent_sequence = define_indent_sequence(indent, _previous_indent)
        return (
            f"{indent_sequence[1:]}{self.__class__.__name__}("
            f"{indent_sequence}{' ' * indent}name={self._name!r}, "
            f"{indent_sequence}{' ' * indent}value={self._value!r})"
        )

    return redefined_repr, convert_to_string


_SVST_Attribute_NameValue.__repr__, \
    _SVST_Attribute_NameValue.convert_to_string = _redefined_combo_Attribute_NameValue()


class SVST_Attribute_Body(_SVST_Attribute_Body):
    __slots__ = ()

    def __init__(self):
        super().__init__()

    @classmethod
    @abstractmethod
    def evaluate_syntax(cls, match_object: re.Match) -> Self:
        return NotImplemented


class SVST_Attribute_Subjects(_SVST_Attribute_Subjects):
    __slots__ = ()

    def __init__(self):
        super().__init__()

    @classmethod
    @abstractmethod
    def evaluate_syntax(cls, match_object: re.Match) -> Self:
        return NotImplemented


class SVST_Attribute_BodySubjects(_SVST_Attribute_BodySubjects):
    __slots__ = ()

    def __init__(self):
        super().__init__()

    @classmethod
    @abstractmethod
    def evaluate_syntax(cls, match_object: re.Match) -> Self:
        return NotImplemented


class SVST_Attribute_Name(_SVST_Attribute_Name):
    __slots__ = ()

    def __init__(self, name: str):
        super().__init__(name)

    @classmethod
    @abstractmethod
    def evaluate_syntax(cls, match_object: re.Match) -> Self:
        return NotImplemented


class SVST_Attribute_Value(_SVST_Attribute_Value):
    __slots__ = ()

    def __init__(self, value: str):
        super().__init__(value)

    @classmethod
    @abstractmethod
    def evaluate_syntax(cls, match_object: re.Match) -> Self:
        return NotImplemented


class SVST_Attribute_NameValue(_SVST_Attribute_NameValue):
    __slots__ = ()

    def __init__(self, name: str, value: str):
        super().__init__(value, name)

    @classmethod
    @abstractmethod
    def evaluate_syntax(cls, match_object: re.Match) -> Self:
        return NotImplemented
