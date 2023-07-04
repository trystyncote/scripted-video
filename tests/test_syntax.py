from tests._syntax_match_functions import match_Create, match_Declare, match_Delete, match_Doctype, match_Metadata, \
    match_Move

import scripted_video.svst as svst

import pytest
import re


class Expected:
    __slots__ = ("__dict__",)  # preventing creation of __weakref__.

    def set(self, name, value):
        """ Wrapper for setting an attribute. """
        self.__setattr__(name, value)  # this is to allow setting an attribute
        # from a string.


@pytest.mark.parametrize("command,cls,match_callable,expected_attr", [
    ("@DOCTYPE scripted-video", svst.Doctype, match_Doctype, "doc:scripted-video"),
    ("HEAD window_width = 852", svst.Metadata, match_Metadata, "name:window_width;value:852"),
    ("SET abc = def AS ghi", svst.Declare, match_Declare, "name:abc;value:def;type:ghi"),
    ("CREATE *obj { x: 100; y: 100; }", svst.Create, match_Create,
     "o_name:*obj;p_name_A:x;p_value_A:100;p_name_B:y;p_value_B:100"),
    ("MOVE *obj { duration: 15; x: 50; y: 50; }", svst.Move, match_Move,
     "o_name:*obj;p_name_A:duration;p_value_A:15;p_name_B:x;p_value_B:50;p_name_C:y;p_value_C:50"),
    ("DELETE OBJECT *obj: val", svst.Delete, match_Delete, "o_name:*obj;p_value:val")
])
def test_syntax_evaluate(command, cls, match_callable, expected_attr):
    expected = Expected()
    for attr in expected_attr.split(";"):
        expected.set(*attr.split(":"))  # assume that the result will be of
        # length 2.

    query = svst.RootNode.syntax_list[cls]
    match = re.match(query, command)
    if match is None:
        assert False
    node = cls.evaluate_syntax(match)
    match_callable(node, expected)


def test_syntax_evaluate_no_match():
    command = "THIS-SHOULD-NOT-MATCH"

    for query in svst.RootNode.syntax_list.values():
        match = re.match(query, command)
        if match is not None:
            assert False
