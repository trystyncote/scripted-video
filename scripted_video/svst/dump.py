from typing import Protocol


class _IndentStr(Protocol):
    def __str__(self, *, indent: int = 0, _previous_indent: int = 0) -> str: ...


def dump(node: _IndentStr, *, indent: int = 0) -> str:
    """ svst Equivalent of ast.dump() """
    # Assume that `node` inherits from `SVST_RootNode`.
    return node.__str__(indent=indent).strip("\n")
