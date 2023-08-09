"""
The _dynamic_attributes module defines a decorator for code generation. This is
a substitution for a former module, _attribute_superclass that doesn't depend
on inheritance.

The reason that I do not use dataclasses directly is because of the fact that
the attributes must be implemented the same throughout all of the nodes. To
prevent breaking the implementation, it must be done in a synchronous manner.
To best accomplish this, they need a shared implementation. This module defines
that behaviour.
"""
import scripted_video.svst._factory_functions as factory_functions

from dataclasses import dataclass, field, MISSING
import enum
from typing import Any


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


class UniversalAttribute(enum.Enum):
    ALL = enum.auto()
    COLUMN_NO = enum.auto()
    END_COLUMN_NO = enum.auto()
    END_LINE_NO = enum.auto()
    LINE_NO = enum.auto()


class WhitespaceAttribute(enum.Enum):
    AFTER_EQUAL_SIGN = enum.auto()
    AFTER_KEYWORD = enum.auto()
    BEFORE_EQUAL_SIGN = enum.auto()


class _AttributeSet:
    __slots__ = ("alias", "annotation", "default", "default_factory", "init", "internal_name", "name")

    def __init__(self, name, annotation, *, alias=None, default: Any = MISSING, default_factory: Any = MISSING,
                 init=True):
        self.name = name
        if alias is None:
            self.alias = name
        else:
            self.alias = alias
        self.annotation = annotation
        self.default = default
        self.default_factory = default_factory
        self.init = init


_attributes = {
    Attribute.BODY: _AttributeSet("body", list, default_factory=list, init=False),
    SpecificAttribute.CONTENTS: _AttributeSet("contents", str),
    SpecificAttribute.DOCTYPE: _AttributeSet("doctype", str),
    Attribute.NAME: _AttributeSet("name", str),
    Attribute.VALUE: _AttributeSet("value", str),
    SpecificAttribute.SCRIPT: _AttributeSet("script", str),
    Attribute.SUBJECTS: _AttributeSet("subjects", list, default_factory=list, init=False),
    Attribute.TYPE: _AttributeSet("type", str),
    WhitespaceAttribute.AFTER_EQUAL_SIGN: _AttributeSet("ws_after_equal_sign", str, alias="ws_ae", default=""),
    WhitespaceAttribute.AFTER_KEYWORD: _AttributeSet("ws_after_keyword", str, alias="ws_ak", default=""),
    WhitespaceAttribute.BEFORE_EQUAL_SIGN: _AttributeSet("ws_before_equal_sign", str, alias="ws_be", default=""),
}


def _create_fn_cts(cls):
    factory_signature = _get_factory_signature(cls)
    try:
        cls.convert_to_string = vars(factory_functions)[factory_signature]()
    except KeyError:
        cls.__has_cts_method__ = False
    else:
        cls.__has_cts_method__ = True


def _define_class(cls):
    for attr in cls.__attributes__:
        attribute = _attributes[attr]
        cls.__annotations__[attribute.name] = attribute.annotation
        _set_attribute_by_field(cls, attribute)

    cls = dataclass(eq=False, frozen=True, slots=True)(cls)
    _create_fn_cts(cls)
    return cls


def _get_factory_signature(cls):
    factory_signature = "factory_StringPrintout__"
    for attr in cls.__attributes__:
        attribute = _attributes[attr]
        factory_signature += f"{attribute.alias}_"
    return factory_signature[:-1]


def _set_attribute_by_field(cls, attribute):
    if attribute.default is not MISSING:
        setattr(cls, attribute.name, field(default=attribute.default, init=attribute.init))
    elif attribute.default_factory is not MISSING:
        setattr(cls, attribute.name, field(default_factory=attribute.default_factory, init=attribute.init))
    else:
        setattr(cls, attribute.name, field(init=attribute.init))


def _set_attributes(cls, name, value):
    if name in cls.__dict__:
        return True
    setattr(cls, name, value)
    return False


def dynamic_attributes(cls=None, /):
    def wrapper():
        return _define_class(cls)

    if cls is None:  # @dynamic_attributes()
        return wrapper

    if not hasattr(cls, "__attributes__"):
        raise _UndefinedAttributesError(f"Class \'{cls.__name__}\' does not define __attributes__.")
    for attr in cls.__attributes__:
        try:
            _attributes[attr]
        except KeyError:
            raise _InvalidAttributesError(f"Class \'{cls.__name__}\' has an undefined attribute: \'{field}\'.")

    return wrapper()  # @dynamic_attributes
