from __future__ import annotations

from scripted_video.parser import script_parser

from scripted_video.objects.ObjectDict import ObjectDict

from scripted_video.qualms.group import QualmGroup

import scripted_video.svst as svst
from scripted_video.svst.neutral_nodes import DoctypeIdentity
from scripted_video.svst.visitor import SVST_NodeVisitor as NodeVisitor

from pathlib import Path
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scripted_video.utils import Options

    from scripted_video.variables.ScriptVariables import ScriptVariables


def _convert_doctype_identity(doctype_identity):
    if doctype_identity is DoctypeIdentity.TIMELINE:
        return svst.TimelineModule


def create_syntax_tree_root(script_name: str):
    return svst.UnknownModule(script_name)


def cycle_over_script(script_file: Path, variables: ScriptVariables, options: Options):
    object_information = ObjectDict()
    syntax_tree = create_syntax_tree_root(str(script_file.name))

    for command_line in script_parser(script_file, block_comment_characters=("/*", "*/"), end_line_character=";",
                                      inline_comment_character="//"):
        syntax_tree = dissect_syntax(command_line.lines[0], syntax_tree)

    navigate_syntax_tree(syntax_tree, object_information, variables, options)

    return object_information


def dissect_syntax(command: str, syntax_tree):
    for _, (respective_class, syntax_command) in syntax_tree.reference.syntax_list.items():
        match = re.match(syntax_command, command)
        if not match:
            continue
        syntax_tree.body.append(respective_class.evaluate_syntax(match))
        if type(syntax_tree) is svst.UnknownModule and any(type(ele) is svst.Doctype for ele in syntax_tree.body):
            doctype_identity = DoctypeIdentity.NONE
            for element in syntax_tree.body:
                if type(element) is svst.Doctype:
                    doctype_identity = element.classify_type()
                    break
            new_module_identity = _convert_doctype_identity(doctype_identity)
            return syntax_tree.transfer(new_module_identity)
        return syntax_tree

    syntax_tree.body.append(svst.UnknownSyntax(command))
    return syntax_tree


def navigate_syntax_tree(syntax_tree, object_information, script_variables, options):
    qualm_group = QualmGroup()

    visitor = NodeVisitor(object_information, script_variables, qualm_group)
    visitor.visit(syntax_tree)

    if qualm_group.has_qualms:
        qualm_group.raise_qualms()

    if options.reveal_syntax_tree or options.debug:
        metadata = script_variables.metadata
        with open(metadata.script_file.parent / f"{Path(metadata.file_name).stem}__svst.txt", "w") as file_pointer:
            file_pointer.write(svst.dump(syntax_tree, indent=4))
