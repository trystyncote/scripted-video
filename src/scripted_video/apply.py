from typing import Any


def apply(expr: type, arg: Any) -> Any:
    """
    A re-implementation of Python 2.0's 'apply' function. This function changes
    the argument 'arg' to the type 'expr'.

    :param expr: The type to be converted into. Do *NOT* use a string
        representation or the like. Use the literal type instead.
    :param arg: The argument to be converted.
    :return: Returns the 'arg' argument as the type 'expr'.
    """
    # Yes, this implementation kinda sucks. I know.
    ''' Non-array types. '''
    if expr is int:
        return int(arg)
    elif expr is float:
        return float(arg)
    elif expr is complex:
        return complex(arg)
    elif expr is str:
        return str(arg)
    elif expr is bytes:
        return bytes(arg)
    elif expr is memoryview:
        return memoryview(bytes(arg))
    elif expr is bool:
        return bool(arg)
    elif expr is range:
        return range(int(arg))

    ''' Array types. '''
    arg = [arg]
    if expr is list:
        return arg
    elif expr is tuple:
        return tuple(arg)
    elif expr is bytearray:
        return bytearray(arg)
    elif expr is set:
        return set(arg)
    elif expr is frozenset:
        return frozenset(arg)
