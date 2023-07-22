def dump(node, *, indent: int = 0):
    """ svst Equivalent of ast.dump() """
    print(node.__str__(indent=indent).strip("\n"))
