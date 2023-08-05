def dump(node, *, indent: int = 0) -> str:
    """ svst Equivalent of ast.dump() """
    # Assume that `node` inherits from `SVST_RootNode`.
    return node.convert_to_string(indent=indent).strip("\n")
