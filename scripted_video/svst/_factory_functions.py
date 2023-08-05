"""
The _factory_functions module is a module that implements a series of factories
that define a '.convert_to_string()' method for any class generated by the
decorator in _dynamic_attributes. This was previously done by code generation,
but this method for constructing it is done mainly for readability and code
maintenance.

All methods that are meant to be retrieved are defined by name as
'factory_StringPrintout__{any $attribute_alias separated by '_'}'.
"""


def _create_string_from_sequence(sequence, name, indent, prev_indent):
    indent_sequence = ""
    if indent > 0:
        indent_sequence = f"\n{' '*prev_indent}"

    if len(sequence) == 0:
        return f"{indent_sequence}{name}=[]"

    return (
        f"{indent_sequence}{' ' * indent}{name}=["
        + ', '.join(node.convert_to_string(indent=indent, _previous_indent=(2*indent)+prev_indent)
                    if getattr(node, "__has_cts_method__", False) else f"{indent_sequence}{' '*(2*indent)}{node!r}"
                    for node in sequence)
        + "]"
    )


'''
# FACTORY LAYOUT
def factory_StringPrintout__():
    def FACTORY(self, *, indent: int = 0, _previous_indent: int = 0) -> str:
        ...

    return FACTORY
'''


def factory_StringPrintout__body_subjects():
    def FACTORY(self, *, indent: int = 0, _previous_indent: int = 0) -> str:
        indent_sequence = ""
        if indent > 0:
            indent_sequence = f"\n{' ' * _previous_indent}"

        return (
            f"{indent_sequence}{self.__class__.__name__}("
            + _create_string_from_sequence(self.body, "body", indent, _previous_indent)
            + ", "
            + _create_string_from_sequence(self.subjects, "subjects", indent, _previous_indent)
            + ")"
        )

    return FACTORY


def factory_StringPrintout__doctype_type():
    def FACTORY(self, *, indent: int = 0, _previous_indent: int = 0) -> str:
        indent_sequence = ""
        if indent > 0:
            indent_sequence = f"\n{' ' * _previous_indent}"

        return (
            f"{indent_sequence}{self.__class__.__name__}("
            f"{indent_sequence}{' ' * indent}doctype={self.doctype!r}, "
            f"{indent_sequence}{' ' * indent}type={self.type!r})"
        )

    return FACTORY


def factory_StringPrintout__name_value():
    def FACTORY(self, *, indent: int = 0, _previous_indent: int = 0) -> str:
        indent_sequence = ""
        if indent > 0:
            indent_sequence = f"\n{' ' * _previous_indent}"

        return (
            f"{indent_sequence}{self.__class__.__name__}("
            f"{indent_sequence}{' ' * indent}name={self.name!r}, "
            f"{indent_sequence}{' ' * indent}value={self.value!r})"
        )

    return FACTORY


def factory_StringPrintout__name_value_type():
    def FACTORY(self, *, indent: int = 0, _previous_indent: int = 0) -> str:
        indent_sequence = ""
        if indent > 0:
            indent_sequence = f"\n{' ' * _previous_indent}"

        return (
            f"{indent_sequence}{self.__class__.__name__}("
            f"{indent_sequence}{' ' * indent}name={self.name!r}, "
            f"{indent_sequence}{' ' * indent}value={self.value!r}, "
            f"{indent_sequence}{' ' * indent}type={self.type!r})"
        )

    return FACTORY


def factory_StringPrintout__name_value_ws_ak_ws_ae_ws_be():
    def FACTORY(self, *, indent: int = 0, _previous_indent: int = 0) -> str:
        indent_sequence = ""
        if indent > 0:
            indent_sequence = f"\n{' ' * _previous_indent}"

        return (
            f"{indent_sequence}{self.__class__.__name__}("
            + f"{indent_sequence}{' ' * indent}name={self.name!r}, "
            + f"{indent_sequence}{' ' * indent}value={self.value!r}, "
            + f"{indent_sequence}{' ' * indent}ws_after_keyword={self.ws_after_keyword!r}, "
            + f"{indent_sequence}{' ' * indent}ws_after_equal_sign={self.ws_after_equal_sign!r}, "
            + f"{indent_sequence}{' ' * indent}ws_before_equal_sign={self.ws_before_equal_sign!r})"
        )

    return FACTORY


def factory_StringPrintout__script_body():
    def FACTORY(self, *, indent: int = 0, _previous_indent: int = 0) -> str:
        indent_sequence = ""
        if indent > 0:
            indent_sequence = f"\n{' ' * _previous_indent}"

        return (
            f"{indent_sequence}{self.__class__.__name__}("
            + f"{indent_sequence}{' '*indent}script={self.script!r}, "
            + _create_string_from_sequence(self.body, "body", indent, _previous_indent)
            + ")"
        )

    return FACTORY
