from __future__ import annotations

from scripted_video.svst._dynamic_attributes import Attribute, dynamic_attributes, SpecificAttribute
from scripted_video.svst.root_node import SVST_RootNode

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import MutableMapping
    import re
    from typing import Self


class NeutralNode(SVST_RootNode):
    __slots__ = ()

    syntax_list: MutableMapping = {}

    def __init_subclass__(cls):
        super().__init_subclass__()
        if hasattr(cls, "_syntax"):
            NeutralNode.syntax_list[cls.__name__] = (cls, cls._syntax)


@dynamic_attributes
class Doctype(NeutralNode):
    __attributes__ = (SpecificAttribute.DOCTYPE,)
    _syntax = r"@DOCTYPE [\s| ]*(scripted-video){1}"
    # syntax = r"@DOCTYPE [\s| ]*(scripted-video){1}[\s| ]+((?:TIMELINE)|(?:MASTER[-]*SCRIPT)|(?:DESIGN)){1};"

    @classmethod
    def evaluate_syntax(cls, match_object: re.Match) -> Self:
        doctype = match_object.group(1)
        class_object = cls(doctype)
        return class_object


@dynamic_attributes
class Object(NeutralNode):
    """
    The Object node refers to a reference to an object, via the approximate
    syntax [*<object>]. The name of the object is referenced as the 'name'.
    Meant to be referred as a subject of another node.
    """
    __attributes__ = (Attribute.NAME,)


@dynamic_attributes
class Property(NeutralNode):
    """
    The Property node refers to a call to a property and its value. The name of
    the property is referenced as the 'name', and its value as 'value'. Meant
    to be referred as a member of the body of another node.
    """
    __attributes__ = (Attribute.NAME, Attribute.VALUE)


@dynamic_attributes
class UnknownSyntax(NeutralNode):
    __attributes__ = (SpecificAttribute.CONTENTS,)
