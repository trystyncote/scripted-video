"""
The _dynamic_attributes module defines a decorator for code generation. This is
a substitution for _attribute_superclass that doesn't depend on inheritance.
_attribute_superclass is not set for complete deletion until no node is
dependent on it. For now, this remains an alternative instead of the default.

The reason that I do not use dataclasses instead of writing this myself, is
that dataclasses doesn't suit my application. All applicable classes need to
define a set of attributes that have a __repr__ and __str__ method, a
convert_to_string method, and have __slots__. Dataclass implementations do
not necessarily work to the use case I need, so I'd rather have it written
myself and prevent repeated code that way.
"""
import enum
import io
import sys


class _InaccessibleAttributeError(Exception):
    pass


class _InvalidAttributesError(Exception):
    pass


class _PredefinedSlotsError(Exception):
    pass


class _UndefinedAttributesError(Exception):
    pass


class Attribute(enum.Enum):
    BODY = enum.auto()
    NAME = enum.auto()
    VALUE = enum.auto()
    SUBJECTS = enum.auto()
    TYPE = enum.auto()


class SpecificAttribute(enum.Enum):
    DOCTYPE = enum.auto()
    CONTENTS = enum.auto()
    SCRIPT = enum.auto()


class WhitespaceAttribute(enum.Enum):
    AFTER_EQUAL_SIGN = enum.auto()
    AFTER_KEYWORD = enum.auto()
    BEFORE_EQUAL_SIGN = enum.auto()


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
        return f"{self.name}: {self.annotation}{f' = {self.default!r}' if self.default is not _NO_DEFAULT else ''}"


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
    Attribute.BODY: _ListAttributeSet("body", list, default_factory=list),
    SpecificAttribute.CONTENTS: _AttributeSet("contents", str),
    SpecificAttribute.DOCTYPE: _AttributeSet("doctype", str),
    Attribute.NAME: _AttributeSet("name", str),
    Attribute.VALUE: _AttributeSet("value", str),
    SpecificAttribute.SCRIPT: _AttributeSet("script", str),
    Attribute.SUBJECTS: _ListAttributeSet("subjects", list, default_factory=list),
    Attribute.TYPE: _AttributeSet("type", str),
    WhitespaceAttribute.AFTER_EQUAL_SIGN: _AttributeSet("ws_after_equal_sign", str, default=""),
    WhitespaceAttribute.AFTER_KEYWORD: _AttributeSet("ws_after_keyword", str, default=""),
    WhitespaceAttribute.BEFORE_EQUAL_SIGN: _AttributeSet("ws_before_equal_sign", str, default=""),
}


def _add_slots(cls):
    # __slots__ cannot be set on a class that already has been created, so a
    # new class needs to be created.

    if "__slots__" in cls.__dict__:
        raise _PredefinedSlotsError(f"Class \'{cls.__name__}\' already specifies __slots__.")

    cls_dict = dict(cls.__dict__)  # Creates a copy of the dictionary to
    # prevent altering the original.
    fields = tuple(_attributes[a].internal_name for a in cls.__attributes__)
    # inherited_slots
    cls_dict["__slots__"] = fields

    for field in cls.__attributes__:
        cls_dict.pop(field, None)
    cls_dict.pop("__dict__", None)

    qualname = getattr(cls, "__qualname__", None)
    cls = cls.__class__(cls.__name__, cls.__bases__, cls_dict)
    if qualname is not None:
        cls.__qualname__ = qualname

    return cls


def _create_dunder_init(cls):
    lines = []
    parameters = []
    for name in cls.__attributes__:
        lines.append(_attributes[name].initialization())
        if _attributes[name].is_parameter:
            parameters.append(_attributes[name])
    return _set_attributes(
        cls,
        "__init__",
        _create_function(
            "__init__",
            ("self", *(a.parameter() for a in parameters)),
            tuple(lines),
            globals_=sys.modules[cls.__module__].__dict__
        )
    )


def _create_dunder_getattribute(cls):
    body = [f"{4*' '}try:", f"{8*' '}return object.__getattribute__(self, item)", f"{4*' '}except AttributeError:",
            f"{8*' '}if item[0] != \"_\":", f"{12*' '}return object.__getattribute__(self, f\"_{{item}}\")",
            f"{8*' '}raise"]
    return _set_attributes(
        cls,
        "__getattribute__",
        _create_function(
            "__getattribute__",
            ("self", "item"),
            tuple(body),
            globals_=sys.modules[cls.__module__].__dict__
        )
    )


def _create_dunder_repr(cls):
    body = io.StringIO()
    body.write(f"{4*' '}return f\"{{self.__class__.__name__}}(")
    for field in cls.__attributes__:
        # TODO: Change behaviour to write differently for sequence objects.
        body.write(f"{_attributes[field].internal_name}={{self.{_attributes[field].internal_name}!r}}, ")
    body = body.getvalue()[:-2] + ")\""
    return _set_attributes(
        cls,
        "__repr__",
        _create_function(
            "__repr__",
            ("self",),
            (body,),
            globals_=sys.modules[cls.__module__].__dict__
        )
    )


def _create_dunder_setattr(cls):
    body = [f"{4*' '}if getattr(self, key, None) is not None:",
            f"{8*' '}from scripted_video.svst._dynamic_attributes import _InaccessibleAttributeError",
            f"{8*' '}raise _InaccessibleAttributeError(f\"Attribute \\\'{{key}}\\\' of class "
            f"\\\'{{self.__class__.__name__}}\\\' is considered immutable.\")",
            f"{4*' '}object.__setattr__(self, key, value)"]
    return _set_attributes(
        cls,
        "__setattr__",
        _create_function(
            "__setattr__",
            ("self", "key", "value"),
            tuple(body),
            globals_=sys.modules[cls.__module__].__dict__
        )
    )


def _create_dunder_str(cls):
    return _set_attributes(
        cls,
        "__str__",
        _create_function(
            "__str__",
            ("self",),
            (f"{4*' '}return self.convert_to_string()",),
            globals_=sys.modules[cls.__module__].__dict__
        )
    )


def _create_function(name, args, body, *, local=None, globals_=None):
    if local is None:
        local = {}

    args = ",".join(args)
    body = "\n".join(f"{4*' '}{b}" for b in body)
    header = f"def {name}({args}):"
    local_vars = ", ".join(local.keys())
    indent = 4 * ' '
    txt = f"def __create_fn__({local_vars}):\n{indent}{header}\n" \
          f"{body}\n{indent}return {name}"
    # def __create_fn__(*local_vars*):
    #     def *generated_function*(*args*):
    #         ...
    #     return *generated_function*

    namespace = {}
    exec(txt, globals_, namespace)
    return namespace["__create_fn__"](**local)


def _create_function_convert_to_string(cls):
    # Basically, this function writes a new function that uses a lot of
    # f-strings. This is particularly unreadable, so I'm including comment
    # representations of what the intended output is.
    lines = []
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

    return _set_attributes(
        cls,
        "convert_to_string",
        _create_function(
            "convert_to_string",
            ("self", "*", "indent: int = 0", "_previous_indent: int = 0"),
            tuple(lines),
            globals_=sys.modules[cls.__module__].__dict__
        )
    )


def _define_class(cls):
    functionalities = [_create_dunder_init, _create_dunder_repr, _create_dunder_str, _create_dunder_getattribute,
                       _create_dunder_setattr, _create_function_convert_to_string]
    for func in functionalities:
        func(cls)
    cls = _add_slots(cls)
    return cls


def _set_attributes(cls, name, value):
    if name in cls.__dict__:
        return True
    setattr(cls, name, value)
    return False


def dynamic_attributes(cls, /):
    if not hasattr(cls, "__attributes__"):
        raise _UndefinedAttributesError(f"Class \'{cls.__name__}\' does not define __attributes__.")
    for field in cls.__attributes__:
        try:
            _attributes[field]
        except KeyError:
            raise _InvalidAttributesError(f"Class \'{cls.__name__}\' has an undefined attribute: \'{field}\'.")

    def wrapper():
        return _define_class(cls)

    return wrapper()
