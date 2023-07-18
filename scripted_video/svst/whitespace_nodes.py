from ._dynamic_attributes import Attribute, dynamic_attributes
from .root_node import SVST_RootNode


@dynamic_attributes
class SimpleWhitespace(SVST_RootNode):
    __attributes__ = (Attribute.VALUE,)

    @property
    def empty(self):
        return bool(self._value)
