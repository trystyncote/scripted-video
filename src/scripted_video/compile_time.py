from src.scripted_video.parser import script_parser

from src.scripted_video.objects.ObjectDict import ObjectDict

from src.scripted_video.qualms.group import QualmGroup

import src.scripted_video.svst as svst

from src.scripted_video.variables.ScriptVariables import ScriptVariables

from pathlib import Path
import re


def create_syntax_tree_root(script_name: str) -> svst.TimelineModule:
    return svst.TimelineModule(script_name)


def cycle_over_script(script_file: Path, variables: ScriptVariables):
    object_information = ObjectDict()
    syntax_tree = create_syntax_tree_root(str(script_file.name))

    for line in script_parser(script_file, block_comment_characters=("/*", "*/"), end_line_character=";",
                              inline_comment_character="//"):
        dissect_syntax(line, syntax_tree)

    navigate_syntax_tree(syntax_tree, object_information, variables)

    return object_information


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
