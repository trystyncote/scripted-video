"""
The _dynamic_attributes module defines a decorator for code generation. This is
a substitution for _attribute_superclass that doesn't depend on inheritance.
_attribute_superclass is not set for complete deletion until no node is
dependent on it. For now, this remains an alternative instead of the default.

The reason that I do not use dataclasses instead of writing this myself, is
that dataclasses doesn't suit my application. All applicable classes need to
define a set of attributes that have a property, a __repr__ and __str__ method,
a convert_to_string method, and have __slots__. Dataclass implementations do
not work to this extent, so I'd rather have it written myself and prevent
repeated code that way.
"""
import inspect
import io
import sys

from ._functions import define_indent_sequence


_ = define_indent_sequence(0, 0)  # Preventing 'unused import' flag. This
# function is required for when the body of a class is evaluated.


class _InvalidAttributesError(Exception):
    pass


class _UndefinedAttributesError(Exception):
    pass


_NO_DEFAULT = object()


class _AttributeSet:
    __slots__ = ("annotation", "default", "internal_name", "name")

    def __init__(self, name, annotation, *, default=_NO_DEFAULT):
        self.name = name
        self.internal_name = f"_{name}"
        self.annotation = annotation.__name__
        self.default = default

    @property
    def is_parameter(self):
        return True

    def initialization(self):
        return f"{4 * ' '}self.{self.internal_name} = {self.name}"

    def parameter(self):
        if not self.is_parameter:
            return ""
        return f"{self.name}: {self.annotation}{f' = {self.default}' if self.default is not _NO_DEFAULT else ''}"

    def property(self):
        property_object = (
            "@property",
            f"def {self.name}(self):",
            f"{4 * ' '}return self.{self.internal_name}"
        )
        return _join_lines(*property_object)


class _ListAttributeSet(_AttributeSet):
    __slots__ = ("default_factory",)

    def __init__(self, name, annotation, *, default=_NO_DEFAULT, default_factory=None):
        super().__init__(name, annotation, default=default)
        self.default_factory = None
        if default_factory is not None:
            self.default = None
            self.default_factory = default_factory()

    @property
    def is_parameter(self):
        return False

    def initialization(self):
        return f"{4*' '}self.{self.internal_name} = {self.default_factory}"


_attributes = {
    "body": _ListAttributeSet("body", list, default_factory=list),
    "name": _AttributeSet("name", str),
    "value": _AttributeSet("value", str),
    "subjects": _ListAttributeSet("subjects", list, default_factory=list),
    "ws_after_equal_sign": _AttributeSet("ws_after_equal_sign", str, default="\'\'"),
    "ws_after_keyword": _AttributeSet("ws_after_keyword", str, default="\'\'"),
    "ws_before_equal_sign": _AttributeSet("ws_before_equal_sign", str, default="\'\'"),
}


def _concatenate_original_body(original_body):
    original_body = [o[4:] for o in original_body]
    return ''.join(original_body)


def _create_dunder_init(cls) -> str:
    lines = [_make_function_header("__init__", *(_attributes[attr] for attr in cls.__attributes__))]
    for name in cls.__attributes__:
        lines.append(_attributes[name].initialization())
    return "\n".join(lines)


def _create_dunder_repr(cls) -> str:
    lines = ["def __repr__(self):"]
    return_statement = io.StringIO()
    return_statement.write(f"{4*' '}return f\"{{self.__class__.__name__}}(")
    for field in cls.__attributes__:
        # TODO: Change behaviour to write differently for sequence objects.
        return_statement.write(f"{_attributes[field].internal_name}={{self.{_attributes[field].internal_name}!r}}, ")
    return_statement = return_statement.getvalue()[:-2] + ")\""
    # return_statement.write(")\"")
    lines.append(return_statement)
    return _join_lines(*lines)


def _create_dunder_slots(cls) -> str:
    fields = []
    for field in cls.__attributes__:
        field_set = _attributes[field]
        if hasattr(field_set, "internal_name"):
            fields.append(field_set.internal_name)
        else:
            fields.append(field_set.name)

    return f"__slots__ = {tuple(fields)!s}"


def _create_dunder_str(cls) -> str:
    return _join_lines("def __str__(self):", f"{4*' '}return self.convert_to_string()")


def _create_function_convert_to_string(cls) -> str:
    # Basically, this function writes a new function that uses a lot of
    # f-strings. This is particularly unreadable, so I'm including comment
    # representations of what the intended output is.
    lines = ["def convert_to_string(self, *, indent: int = 0, _previous_indent: int = 0) -> str:"]
    attributes = cls.__attributes__

    if len(attributes) == 0:
        lines.append(f"{4*' '}return f\'{{\" \" * _previous_indent}}{{self.__class__.__name__}}()\'")
        # def convert_to_string(self, *, indent: int = 0, _previous_indent: int = 0) -> str:
        #     return f'{" " * _previous_indent}{self.__class__.__name__}()'

    elif len(attributes) == 1:
        attr = _attributes[attributes[0]]
        if type(attr.annotation) == list:
            new_lines = [
                f"{4 * ' '}if len(self.{attr.internal_name}) == 0:",
                f"{8 * ' '}return f\'{{\" \" * _previous_indent}}{{self.__class__.__name__}}"
                f"({attr.name}={{self.{attr.internal_name}}})\'",
                f"{4 * ' '}return (",
                f"{8 * ' '}f\'{{\" \" * _previous_indent}}{{self.__class__.__name__}}(\'",
                f"{8 * ' '}+ create_string_from_sequence(self.{attr.internal_name}, \'{attr.name}\', "
                f"indent, indent + _previous_indent)",
                f"{8 * ' '}+ \')\'",
                f"{4 * ' '})"
            ]
            # def convert_to_string(self, *, indent: int = 0, _previous_indent: int = 0) -> str:
            #     if len(self.<sequence>) == 0:
            #         return f"{' ' * _previous_indent}{self.__class__.__name__}(<sequence>={self.<sequence>})"
            #     return (
            #         f"{' ' * _previous_indent}{self.__class__.__name__}("
            #         + create_string_from_sequence(self.<sequence>, "<sequence>", indent, indent + _previous_indent)
            #         + ")"
            #     )
        else:
            new_lines = [
                f"{4 * ' '}return f\'{{\" \" * _previous_indent}}{{self.__class__.__name__}}({attr.name}="
                f"{{self.{attr.internal_name}!r}})\'"
            ]
            # def convert_to_string(self, *, indent: int = 0, _previous_indent: int = 0) -> str:
            #     return f'{" " * _previous_indent}{self.__class__.__name__}(<name>={self.<name>})'

        for new_line in new_lines:
            lines.append(new_line)

    else:
        lines.append(f"{4*' '}indent_sequence = define_indent_sequence(indent, _previous_indent)")
        lines.append(f"{4*' '}return (")
        lines.append(f"{8*' '}f\"{{\' \' * _previous_indent}}{{self.__class__.__name__}}(\"")
        for a in attributes:
            attr = _attributes[a]
            if type(attr.annotation) == list:
                lines.append(f"{8*' '}+ (create_string_from_sequence(self.{attr.internal_name}, \"{attr.name}\", "
                             f"indent, indent + _previous_indent)")
                lines.append(f"{11*' '}if len(self.{attr.internal_name} != 0 else f\'{{\" \" * _previous_indent}}"
                             f"{attr.name}=[]\'))")
            else:
                lines.append(f"{8*' '}+ f\'{{indent_sequence}}{{\" \" * indent}}{attr.name}"
                             f"={{self.{attr.internal_name}!r}}\'")

            lines.append(f"{8*' '}+ \', \'")

        lines.pop(-1)
        lines.append(f"{8*' '}+ \')\'")
        lines.append(f"{4*' '})")
        # def convert_to_string(self, *, indent: int = 0, _previous_indent: int = 0) -> str:
        #     return (
        #         f"{' ' * _previous_indent}{self.__class__.__name__}("
        #         + (create_string_from_sequence(self.<sequence>, "<sequence>", indent, indent + _previous_indent)
        #            if len(self.<sequence> != 0 else f"{' ' * _previous_indent}<sequence>=[]"))  # for sequence objects
        #         + ", "
        #         + f"{' ' * _previous_indent}<name>={self.<name>}"  # for non-sequence objects
        #         + ")"
        #     )

    return _join_lines(*lines)


def _create_function_properties(cls) -> str:
    properties = []
    for field in cls.__attributes__:
        field_set = _attributes[field]
        if hasattr(field_set, "internal_name"):
            properties.append(field)

    if not properties:
        return ""

    return '\n\n'.join(f"{_attributes[p].property()}" for p in properties)


def _define_class(cls):
    original_module = cls.__module__
    name = cls.__name__
    bases = cls.__bases__
    namespace = type.__prepare__(name, bases)
    body = _write_body(cls)
    exec(body, sys.modules[cls.__module__].__dict__, namespace)
    cls = type(name, bases, namespace)
    cls.__module__ = original_module
    return cls


def _join_lines(*lines):
    return "\n".join(lines)


def _make_function_header(function_name, *parameter_attribute):
    return f"def {function_name}(self, {', '.join(attr.parameter() for attr in parameter_attribute).strip(', ')}):"


def _write_body(cls):
    functionalities = [_create_dunder_slots, _create_dunder_init, _create_dunder_repr, _create_dunder_str,
                       _create_function_properties, _create_function_convert_to_string]
    body = io.StringIO()
    for func in functionalities:
        body.write(func(cls))
        body.write("\n\n")
    body.write(_concatenate_original_body(inspect.getsourcelines(cls)[0][2:]))
    return body.getvalue()


def dynamic_attributes(cls, /):
    if not hasattr(cls, "__attributes__"):
        raise _UndefinedAttributesError(f"Class \'{cls.__name__}\' does not define __attributes__.")

    def wrapper():
        return _define_class(cls)

    return wrapper()
