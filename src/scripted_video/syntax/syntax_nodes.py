from src.scripted_video.syntax._attribute_superclass import _SVST_Attribute_Body, _SVST_Attribute_BodySubjects, \
    _SVST_Attribute_Name, _SVST_Attribute_NameValue
from src.scripted_video.syntax._functions import create_string_from_sequence, define_indent_sequence, gatekeep_indent

from abc import abstractmethod
from re import Match as re_Match
from typing import Self


class Metadata(_SVST_Attribute_NameValue):
    """
    The Metadata node refers to the HEAD keyword. The syntax looks
    approximately as follows:

    HEAD <attribute> = <value>;

    Previous syntax will soon be deprecated, and converted into:

    META <attribute> = <value>;
    """
    __slots__ = ()
    # _syntax = r"META ([\w_]+)[\s| ]*={1}[\s| ]*([\w_]+)"
    _syntax = r"HEAD ([\w_]+)[\s| ]*={1}[\s| ]*([\w_]+)"

    @classmethod
    def evaluate_syntax(cls, match_object: re_Match) -> Self:
        attribute_name = match_object.group(1)
        attribute_value = match_object.group(2)
        return cls(attribute_name, attribute_value)


class Declare(_SVST_Attribute_NameValue):
    """
    The Declare node refers to the SET keyword. The syntax looks
    approximately as follows:

    SET <variable-name> = <value> AS <type>;

    Previous syntax will soon be deprecated, and converted into:

    DECLARE <type> <variable-name> = <value>;
    """
    __slots__ = ("_type",)
    # _syntax = r"DECLARE ([\w_]+)[\s| ]{1}([\w_]+)[\s| ]*={1}[\s| ]*([\w_]_)"
    _syntax = r"SET ([\w_]+)[\s| ]*=[\s| ]*([\w_]+)[\s| ]* AS ([\w_]+)"

    def __init__(self, name: str, value: str, type_: str):
        super().__init__(name, value)
        self._type = type_

    def __repr__(self):
        return f"{self.__class__.__name__}(_name={self._name}, _value={self._value}, _type={self._type})"

    @property
    def type(self) -> str:
        return self._type

    def convert_to_string(self, *, indent: int = 0, _previous_indent: int = 0) -> str:
        gatekeep_indent(indent)
        indent_sequence = define_indent_sequence(indent, _previous_indent)
        return (
            f"{indent_sequence[1:]}{self.__class__.__name__}("
            f"{indent_sequence}{' ' * indent}name={self._name!r}, "
            f"{indent_sequence}{' ' * indent}value={self._value!r}, "
            f"{indent_sequence}{' ' * indent}type={self._type!r}"
            f"{indent_sequence})"
        )

    @classmethod
    def evaluate_syntax(cls, match_object: re_Match) -> Self:
        variable_name = match_object.group(1)
        variable_value = match_object.group(2)
        variable_type = match_object.group(3)
        return cls(variable_name, variable_value, variable_type)


class Object(_SVST_Attribute_Name):
    """
    The Object node refers to a reference to an object, via the approximate
    syntax [*<object>]. The name of the object is referenced as the 'name'.
    Meant to be referred as a subject of another node.
    """
    __slots__ = ()

    @classmethod
    @abstractmethod
    def evaluate_syntax(cls, match_object: re_Match) -> Self:
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
    def evaluate_syntax(cls, match_object: re_Match) -> Self:
        return NotImplemented


class Create(_SVST_Attribute_BodySubjects):
    """
    The Create node refers to the 'CREATE' keyword. The syntax looks
    approximately as follows:

    CREATE <object>: <keywords>, ...;

    Previous syntax will soon be deprecated, and converted into:

    CREATE *<object>[, *<object> ...] {
        <property>: <value>; ...
    };
    """
    __slots__ = ()
    _syntax = r"CREATE OBJECT ([\w\-_]+):[\s| ]*((?:[\w\s\$\-_\/.]*,[\s| ]){5}[\w\s\$\-_\/.]*)"

    @classmethod
    def evaluate_syntax(cls, match_object: re_Match) -> Self:
        class_object = cls()
        class_object.subjects.append(Object(match_object.group(1)))

        properties_expected = ["file-name", "start-time", "x", "y", "scale", "layer"]
        properties_literal = match_object.group(2).split(",")

        for name, value in zip(properties_expected, properties_literal, strict=True):
            class_object.body.append(Property(name, value.strip()))

        return class_object


class Move(_SVST_Attribute_BodySubjects):
    """
    The Move node refers to the 'MOVE' keyword. The syntax looks approximately
    as follows:

    MOVE <object>: <keywords>, ...;

    Previous syntax will soon be deprecated, and converted into:

    MOVE *<object>[, *<object> ...] <function>(<parameters>, ...);
    """
    __slots__ = ()
    _syntax = r"MOVE OBJECT ([\w\-_]+):[\s| ]*((?:[\w\s\$\-_\/.]*,[\s| ]){4}[\w\s\$\-_\/.]*)"

    # _syntax = r"MOVE (\*[\w_]*[,(\s| )\*[\w_]*]*)[\s| ]([\w_]*[(](\${1}[\w_]*(?:,(?:\s| )\${1}[\w_]*)*)*[)](?:," \
    #           r"(?:\s| )[\w_]*[(](\${1}[\w_]*(?:,(?:\s| )\${1}[\w_]*)*)*[)])*);"

    @classmethod
    def evaluate_syntax(cls, match_object: re_Match) -> Self:
        """
        The MOVE keyword will eventually be changed to call a movement function
        on its object starting at its call time. This will not be the same as
        current functionality. Ex.

        MOVE *object %linear(new-x, new-y) over 30s;

        (or something like that.)
        """
        class_object = cls()
        class_object.subjects.append(Object(match_object.group(1)))

        properties_expected = ["move-time", "move-x", "move-y", "move-scale", "move-rate"]
        properties_literal = match_object.group(2).split(",")

        for name, value in zip(properties_expected, properties_literal, strict=True):
            class_object.body.append(Property(name, value.strip()))

        return class_object


class Delete(_SVST_Attribute_BodySubjects):
    """
    The Delete node refers to the 'DELETE' keyword. The syntax looks
    approximately as follows:

    DELETE <object>: <keywords>, ...

    Deprecated functionality and will eventually be deleted.
    """
    __slots__ = ()
    _syntax = r"DELETE OBJECT ([\w\-_]+):[\s| ]*([\w\s\$\-_\/.]*)"

    @classmethod
    def evaluate_syntax(cls, match_object: re_Match) -> Self:
        class_object = cls()
        class_object.subjects.append(Object(match_object.group(1)))
        value = match_object.group(2)
        class_object.body.append(Property("delete-time", value.strip()))
        return class_object


class TimelineModule(_SVST_Attribute_Body):
    """
    The TimelineModule node is the outermost member of the syntax tree (similar
    to the 'Module' node of the built-in AST). It has a body attribute that is
    meant to carry all of the blocks in the given script. The script's name
    (without suffix) is referred to as the 'script_name' attribute.
    """
    __slots__ = ("_script",)

    def __init__(self, script_name: str):
        super().__init__()
        self._script = script_name

    def __repr__(self):
        return f"{self.__class__.__name__}(_body={[node.__class__.__name__ for node in self._body]}, " \
               f"_script={self._script!r})"

    @property
    def script_name(self) -> str:
        return self._script

    def convert_to_string(self, *, indent: int = 0, _previous_indent: int = 0) -> str:
        gatekeep_indent(indent)
        indent_sequence = define_indent_sequence(indent, _previous_indent)
        return (
            f"{' ' * _previous_indent}{self.__class__.__name__}("
            + create_string_from_sequence(self._body, "body", indent, indent + _previous_indent)
            + ", "
              f"{indent_sequence}{' ' * indent}script_name={self._script!r}"
              f"{indent_sequence})"
        )

    @classmethod
    @abstractmethod
    def evaluate_syntax(cls, match_object: re_Match) -> Self:
        return NotImplemented
