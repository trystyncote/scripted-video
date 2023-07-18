from ._attribute_superclass import SVST_Attribute_Body, SVST_Attribute_BodySubjects, SVST_Attribute_NameValue
from ._dynamic_attributes import Attribute, dynamic_attributes, WhitespaceAttribute
from ._functions import create_string_from_sequence, define_indent_sequence, gatekeep_indent
from .neutral_nodes import Object, Property
from .root_node import SVST_RootNode

from abc import abstractmethod
from collections.abc import MutableMapping
import re
from typing import Self


class TimelineNode(SVST_RootNode):
    __slots__ = ()

    syntax_list: MutableMapping = {}

    def __init_subclass__(cls):
        super().__init_subclass__()
        if hasattr(cls, "_syntax"):
            TimelineNode.syntax_list[cls.__name__] = (cls, cls._syntax)


@dynamic_attributes
class Metadata(TimelineNode):
    """
    The Metadata node refers to the HEAD keyword. The syntax looks
    approximately as follows:

    HEAD <attribute> = <value>;

    Previous syntax will soon be deprecated, and converted into:

    META <attribute> = <value>;
    """
    __attributes__ = (Attribute.NAME, Attribute.VALUE, WhitespaceAttribute.AFTER_KEYWORD,
                      WhitespaceAttribute.AFTER_EQUAL_SIGN, WhitespaceAttribute.BEFORE_EQUAL_SIGN)
    # _syntax = r"META ([\w_]+)[\s| ]*={1}[\s| ]*([\w_]+)"
    _syntax = r"HEAD ([\s|]*)([\w_]+)([\s| ]*)={1}([\s| ]*)([\w_]+)"

    @classmethod
    def evaluate_syntax(cls, match_object: re.Match) -> Self:
        whitespace_after_keyword = match_object.group(1)
        attribute_name = match_object.group(2)
        whitespace_before_equal = match_object.group(3)
        whitespace_after_equal = match_object.group(4)
        attribute_value = match_object.group(5)
        return cls(attribute_name, attribute_value, whitespace_after_keyword, whitespace_after_equal,
                   whitespace_before_equal)


@dynamic_attributes
class Declare(TimelineNode):
    """
    The Declare node refers to the SET keyword. The syntax looks
    approximately as follows:

    DECLARE <type> <variable-name> = <value>;
    """
    __attributes__ = (Attribute.NAME, Attribute.VALUE, Attribute.TYPE)
    _syntax = r"DECLARE ([\w_]+)[\s|]+([\w_]+)[\s|]*={1}[\s|]*([\w\s_!.,\"]+)"

    @classmethod
    def evaluate_syntax(cls, match_object: re.Match) -> Self:
        variable_type = match_object.group(1)
        variable_name = match_object.group(2)
        variable_value = match_object.group(3)
        return cls(variable_name, variable_value, variable_type)


@dynamic_attributes
class Create(TimelineNode):
    """
    The Create node refers to the 'CREATE' keyword. The syntax looks
    approximately as follows:

    CREATE *<object> {
        <property>: <value>; ...
    };
    """
    __attributes__ = (Attribute.BODY, Attribute.SUBJECTS)
    _syntax = r"CREATE (\*[\w_-]*)[\s|]*{([\w\s_\-;:.$\/]*)}"
    _sub_syntax = r"([\w_-]+)[\s|]*:[\s|]*([\w$\/\-_\. ]+)[\s|]*;"

    @classmethod
    def evaluate_syntax(cls, match_object: re.Match) -> Self:
        class_object = cls()
        class_object.subjects.append(Object(match_object.group(1)))

        property_string = match_object.group(2)
        for property_pattern in re.finditer(cls._sub_syntax, property_string):
            name = property_pattern.group(1)
            value = property_pattern.group(2)
            class_object.body.append(Property(name, value))

        return class_object


@dynamic_attributes
class Move(TimelineNode):
    """
    The Move node refers to the 'MOVE' keyword. The syntax looks approximately
    as follows:

    MOVE *<object> {
        <property>: <value>; ...
    };
    """
    __attributes__ = (Attribute.BODY, Attribute.SUBJECTS)
    _syntax = r"MOVE (\*[\w_]*[,(\s| )\*[\w_]*]*)[\s| ]{([\w\s_\-;:.$\/]*)}"
    _sub_syntax = r"([\w_-]+)[\s|]*:[\s|]*([\w$\/\-_\. ]+)[\s|]*;"

    @classmethod
    def evaluate_syntax(cls, match_object: re.Match) -> Self:
        class_object = cls()
        class_object.subjects.append(Object(match_object.group(1)))

        property_string = match_object.group(2)
        for property_pattern in re.finditer(cls._sub_syntax, property_string):
            name = property_pattern.group(1)
            value = property_pattern.group(2)
            class_object.body.append(Property(name, value))

        return class_object


@dynamic_attributes
class Delete(TimelineNode):
    """
    The Delete node refers to the 'DELETE' keyword. The syntax looks
    approximately as follows:

    DELETE <object>: <keywords>, ...

    Deprecated functionality and will eventually be deleted.
    """
    __attributes__ = (Attribute.BODY, Attribute.SUBJECTS)
    _syntax = r"DELETE OBJECT (\*[\w\-_]+):[\s| ]*([\w\s\$\-_\/.]*)"

    @classmethod
    def evaluate_syntax(cls, match_object: re.Match) -> Self:
        class_object = cls()
        class_object.subjects.append(Object(match_object.group(1)))
        value = match_object.group(2)
        class_object.body.append(Property("delete-time", value.strip()))
        return class_object


class TimelineModule(SVST_Attribute_Body):
    """
    The TimelineModule node is the outermost member of the svst tree (similar
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
              f"{indent_sequence}{' ' * indent}script_name={self._script!r})"
        )

    @classmethod
    @abstractmethod
    def evaluate_syntax(cls, match_object: re.Match) -> Self:
        return NotImplemented
