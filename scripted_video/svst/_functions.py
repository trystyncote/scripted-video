from collections.abc import MutableSequence
from io import StringIO


def create_string_from_sequence(sequence: MutableSequence, name: str, indent: int, prev_indent: int) -> str:
    indent_sequence = define_indent_sequence(indent, prev_indent)
    if len(sequence) == 0:
        return f"{indent_sequence}{name}=[]"
    elif len(sequence) == 1:
        return (
            f"{indent_sequence}{name}=["
            + sequence[0].convert_to_string(indent=indent, _previous_indent=indent+prev_indent).strip()
            + "]"
        )

    string = StringIO()
    string.write(f"{indent_sequence}{name}=[")
    for element in sequence:
        if indent > 0:
            string.write("\n")
        string.write(element.convert_to_string(indent=indent, _previous_indent=indent+prev_indent))
        if sequence[-1] is not element:
            string.write(", ")
    string.write("]")
    return string.getvalue()


def define_indent_sequence(indent: int, prev_indent: int) -> str:
    if indent == 0:
        return ""
    else:
        return f"\n{' '*prev_indent}"


def gatekeep_indent(indent: int) -> None:
    if type(indent) != int:
        raise TypeError("Attribute 'indent' must be an integer.")
    if indent < 0:
        raise ValueError("Attribute 'indent' must be a positive integer.")
