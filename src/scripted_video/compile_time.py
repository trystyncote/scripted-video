import src.scripted_video.svst as svst

from src.scripted_video.qualms.group import QualmGroup

import re


def create_syntax_tree_root(script_name: str) -> svst.TimelineModule:
    return svst.TimelineModule(script_name)


def dissect_syntax(command: str, syntax_tree):
    for respective_class, syntax_command in svst.RootNode.syntax_list.items():
        match = re.match(syntax_command, command)
        if not match:
            continue
        syntax_tree.body.append(respective_class.evaluate_syntax(match))
        return


def navigate_syntax_tree(syntax_tree, object_information, script_variables):
    qualm_group = QualmGroup()

    visitor = svst.NodeVisitor(object_information, script_variables, qualm_group)
    visitor.visit(syntax_tree)

    if qualm_group.has_qualms:
        qualm_group.raise_qualms()
