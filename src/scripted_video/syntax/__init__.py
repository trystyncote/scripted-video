from .root_node import SVST_RootNode as RootNode
from .syntax_nodes import Create, Declare, Delete, Metadata, Move, Object, Property, TimelineModule
from .visitor import SVST_NodeVisitor as NodeVisitor


def _():
    a1 = RootNode()
    a2 = Create()
    a3 = Declare("x", "y", "z")
    a31 = Delete()
    a4 = Metadata("x", "y")
    a5 = Move()
    a6 = Object("x")
    a7 = Property("x", "y")
    a8 = TimelineModule("x")
    a9 = NodeVisitor()
    print(a1, a2, a3, a31, a4, a5, a6, a7, a8, a9)
