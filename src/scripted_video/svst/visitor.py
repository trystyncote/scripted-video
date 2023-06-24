"""
This module takes implementation inspiration from Python's built-in 'ast'
module. This code acts very closely to the built-in module because of a very
similar tree-like structure. This was a deliberate design choice. Credit to the
original source.
"""
from .syntax_nodes import Object, Property
from .root_node import SVST_RootNode

from src.scripted_video.objects.ImageObject import ImageObject
from src.scripted_video.objects.instruction import MoveInstruction

from src.scripted_video.qualms.crash import DoctypeNotAtBeginning

from pathlib import Path
from typing import Callable


def _iter_fields(node):
    """ Based on the built-in equivalent of 'ast.iter_fields()'. """
    for attr in dir(node):
        if attr.startswith("__") and attr.endswith("__"):
            continue
        if type(attr) == Callable:
            continue
        yield getattr(node, attr)


class SVST_NodeVisitor:
    __slots__ = ("_objects", "_variables", "_qualms")

    def __init__(self, objects, variables, qualms):
        self._objects = objects
        self._variables = variables
        self._qualms = qualms

    def visit(self, node, /):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node, /):
        for attribute in _iter_fields(node):
            if isinstance(attribute, list):
                for item in attribute:
                    if isinstance(item, SVST_RootNode):
                        self.visit(item)
            elif isinstance(attribute, SVST_RootNode):
                self.visit(attribute)

    def visit_Create(self, node, /):
        for subject in node.subjects:
            if not isinstance(subject, Object):
                continue
            new_object = ImageObject(subject.name)
            new_object.init_variables_instance(self._variables)
            self._objects[subject.name] = new_object

            for body_element in node.body:
                if not isinstance(body_element, Property):
                    continue
                new_object.add_property(body_element.name, body_element.value)

        return self.generic_visit(node)

    def visit_Declare(self, node, /):
        name = node.name
        value = node.value
        type_ = node.type

        if type_ == "ADDRESS":
            if value == "__current_address__":
                value = self._variables.metadata.script_file.parent
            else:
                value = Path(str(value))

        elif type_ == "BOOL":
            assert isinstance(value, str)  # This 'assert' keyword is here to
            # prevent mypy from raising a [union-attr] error.
            if value.upper() == "TRUE":
                value = True
            elif value.upper() == "FALSE":
                value = False
            else:
                pass  # TODO: Add error handling for when the value is invalid when type is BOOL.

        elif type_ == "FLOAT":
            value = float(str(value))

        elif type_ == "INT":
            value = int(str(value))

        elif type_ == "STRING":
            pass  # This section does nothing but allow the script to not evaluate
            # the 'else' clause, which is for raising an error for when `type_` is
            # invalid.

        else:
            pass  # TODO: Add error handling for when type attribute of Declare is invalid.

        self._variables.constants.call_relevant(type_).create_variable(name, value)

        return self.generic_visit(node)

    def visit_Delete(self, node, /):
        for subject in node.subjects:
            if not isinstance(subject, Object):
                continue
            if subject.name not in self._objects:
                continue  # TODO: Add error handling for when Delete is called before Create.
            relevant_object = self._objects[subject.name]

            for body_element in node.body:
                if not isinstance(body_element, Property):
                    continue
                relevant_object.add_property(body_element.name, body_element.value)

        return self.generic_visit(node)

    def visit_Metadata(self, node, /):
        name = node.name
        value = node.value

        if name in ("frame_rate", "window_height", "window_width"):
            value = int(value)

        self._variables.metadata.update_value(name, value)

        return self.generic_visit(node)

    def visit_Move(self, node, /):
        for subject in node.subjects:
            if not isinstance(subject, Object):
                continue
            if subject.name not in self._objects:
                continue  # TODO: Add error handling for when Move is called before Create.
            instruction = MoveInstruction(subject.name, self._variables.metadata.frame_rate)

            for body_element in node.body:
                if not isinstance(body_element, Property):
                    continue
                instruction.set_attribute(body_element.name, body_element.value)

            self._objects[subject.name].add_adjustment(instruction)

        return self.generic_visit(node)

    def visit_TimelineModule(self, node, /):
        DoctypeNotAtBeginning.check(node, self._qualms)

        return self.generic_visit(node)
