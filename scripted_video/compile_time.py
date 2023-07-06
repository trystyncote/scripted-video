from scripted_video.parser import script_parser
from scripted_video.utils import Options

from scripted_video.objects.ObjectDict import ObjectDict

from scripted_video.qualms.crash import DoctypeNotAtBeginning
from scripted_video.qualms.group import QualmGroup

import scripted_video.svst as svst
from scripted_video.svst.visitor import SVST_NodeVisitor as NodeVisitor

from scripted_video.variables.ScriptVariables import ScriptVariables

from pathlib import Path
import re


def create_syntax_tree_root(script_name: str) -> svst.TimelineModule:
    return svst.TimelineModule(script_name)


def cycle_over_script(script_file: Path, variables: ScriptVariables, options: Options):
    object_information = ObjectDict()
    syntax_tree = create_syntax_tree_root(str(script_file.name))

    for line in script_parser(script_file, block_comment_characters=("/*", "*/"), end_line_character=";",
                              inline_comment_character="//"):
        dissect_syntax(line, syntax_tree)

    navigate_syntax_tree(syntax_tree, object_information, variables, options)

    return object_information


def dissect_syntax(command: str, syntax_tree):
    if not syntax_tree.body:
        match = re.match(svst.Doctype.syntax, command)
        if match:
            syntax_tree.body.append(svst.Doctype.evaluate_syntax(match))
            return
        else:
            DoctypeNotAtBeginning().raise_qualms()

    for respective_class, syntax_command in svst.TimelineNode.syntax_list.items():
        match = re.match(syntax_command, command)
        if not match:
            continue
        syntax_tree.body.append(respective_class.evaluate_syntax(match))
        return

    syntax_tree.body.append(svst.UnknownSyntax(command))


def navigate_syntax_tree(syntax_tree, object_information, script_variables, options):
    if options.debug:
        print(":: Generated Syntax Tree:")
        print(syntax_tree.convert_to_string(indent=4))
        print("")

    qualm_group = QualmGroup()

    visitor = NodeVisitor(object_information, script_variables, qualm_group)
    visitor.visit(syntax_tree)

    if qualm_group.has_qualms:
        qualm_group.raise_qualms()
