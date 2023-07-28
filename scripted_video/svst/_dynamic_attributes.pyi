import enum
from typing import overload, Protocol, runtime_checkable, TypeVar


class Attribute(enum.Enum):
    BODY = ...
    NAME = ...
    VALUE = ...
    SUBJECTS = ...
    TYPE = ...

class SpecificAttribute(enum.Enum):
    DOCTYPE = ...
    CONTENTS = ...
    SCRIPT = ...

class WhitespaceAttribute(enum.Enum):
    AFTER_EQUAL_SIGN = ...
    AFTER_KEYWORD = ...
    BEFORE_EQUAL_SIGN = ...


ANY_ATTRIBUTE = Attribute | SpecificAttribute | WhitespaceAttribute


class _OriginalStructure(Protocol):
    __attributes__: tuple[ANY_ATTRIBUTE, ...] = ...


_CLASS = TypeVar("_CLASS", bound=_OriginalStructure)


@runtime_checkable
class _RewrittenStructure(Protocol):
    __attributes__: tuple[ANY_ATTRIBUTE, ...] = ...
    __slots__: tuple[str, ...] | str = ...

    @overload
    def __init__(self): ...
    @overload
    def __init__(self, contents: str): ...
    @overload
    def __init__(self, doctype: str): ...
    @overload
    def __init__(self, name: str): ...
    @overload
    def __init__(self, name: str, value: str): ...
    @overload
    def __init__(self, name: str, value: str, type: str): ...
    @overload
    def __init__(self, name: str, value: str, ws_after_keyword: str = "", ws_after_equal_sign: str = "",
                 ws_before_equal_sign: str = ""): ...
    @overload
    def __init__(self, value: str): ...

    def __repr__(self): ...
    def __str__(self, *, indent: int = 0, _previous_indent: int = 0): ...
    def __getattribute__(self, item): ...
    def __setattr__(self, key, value): ...


_UPDATED_CLASS = TypeVar("_UPDATED_CLASS", bound=_RewrittenStructure)


@overload
def dynamic_attributes(cls: type[_CLASS]) -> _UPDATED_CLASS: ...
