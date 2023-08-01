from scripted_video.svst._dynamic_attributes import Attribute, dynamic_attributes
from scripted_video.svst.root_node import SVST_RootNode


@dynamic_attributes
class SimpleWhitespace(SVST_RootNode):
    __attributes__ = (Attribute.VALUE,)

    @property
    def empty(self):
        return bool(self._value)
