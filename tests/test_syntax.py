from tests._syntax_match_functions import match_Create, match_Declare, match_Doctype, match_Metadata

from src.scripted_video.syntax.root_node import SVST_RootNode as RootNode
from src.scripted_video.syntax.syntax_nodes import Create, Declare, Doctype, Metadata

import pytest
import re


class Expected:
    __slots__ = ("__dict__",)  # preventing creation of __weakref__.

    def set(self, name, value):
        """ Wrapper for setting an attribute. """
        self.__setattr__(name, value)  # this is to allow setting an attribute
        # from a string.


@pytest.mark.parametrize("command,cls,match_callable,expected_attr", [
    ("@DOCTYPE scripted-video", Doctype, match_Doctype, "doc:scripted-video"),
    ("HEAD window_width = 852", Metadata, match_Metadata, "name:window_width;value:852"),
    ("SET abc = def AS ghi", Declare, match_Declare, "name:abc;value:def;type:ghi"),
    ("CREATE *obj { x: 100; y: 100; }", Create, match_Create,
     "o_name:*obj;p_name_A:x;p_value_A:100;p_name_B:y;p_value_B:100")
])
def test_syntax_evaluate(command, cls, match_callable, expected_attr):
    expected = Expected()
    for attr in expected_attr.split(";"):
        expected.set(*attr.split(":"))  # assume that the result will be of
        # length 2.

    query = RootNode.syntax_list[cls]
    match = re.match(query, command)
    if match is None:
        assert False
    node = cls.evaluate_syntax(match)
    match_callable(node, expected)
