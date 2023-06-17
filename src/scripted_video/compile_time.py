import src.scripted_video.syntax as svSyntax

import re


def create_syntax_tree_root(script_name: str) -> svSyntax.TimelineModule:
    return svSyntax.TimelineModule(script_name)


def dissect_syntax(command: str, syntax_tree):
    for respective_class, syntax_command in svSyntax.RootNode.syntax_list:
        match = re.match(syntax_command, command)
        if not match:
            continue
        syntax_tree.body.append(respective_class.evaluate_syntax(match))
        return


def navigate_syntax_tree(syntax_tree, object_information, script_variables):
    visitor = svSyntax.NodeVisitor()
    visitor.visit(
        syntax_tree,
        objects=object_information,
        variables=script_variables
    )