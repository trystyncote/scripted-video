from ._dynamic_attributes import Attribute, dynamic_attributes, SpecificAttribute
from .root_node import SVST_RootNode

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


@dynamic_attributes
class Property(SVST_RootNode):
    """
    The Property node refers to a call to a property and its value. The name of
    the property is referenced as the 'name', and its value as 'value'. Meant
    to be referred as a member of the body of another node.
    """
    __attributes__ = (Attribute.NAME, Attribute.VALUE)


@dynamic_attributes
class UnknownSyntax(SVST_RootNode):
    __attributes__ = (SpecificAttribute.CONTENTS,)
