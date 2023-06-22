from tests._syntax_match_functions import match_Declare, match_Doctype, match_Metadata

from src.scripted_video.syntax.root_node import SVST_RootNode as RootNode
from src.scripted_video.syntax.syntax_nodes import Declare, Doctype, Metadata

import pytest
import re


@pytest.mark.parametrize("command,cls,match_callable", [
    ("@DOCTYPE scripted-video", Doctype, match_Doctype),
    ("HEAD window_width = 852", Metadata, match_Metadata),
    ("SET abc = def AS ghi", Declare, match_Declare)
])
def test_syntax_evaluate(command, cls, match_callable):
    query = RootNode.syntax_list[cls]
    match = re.match(query, command)
    if match is None:
        assert False
    node = cls.evaluate_syntax(match)
    match_callable(node)
