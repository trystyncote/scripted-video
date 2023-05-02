from src.scripted_video.variables._type import TypeAddress, TypeBool, TypeFloat, TypeInt, TypeString


class ConstantVariables:
    # I am well aware that this is boilerplate-level code and that it may be
    # easier to use dataclasses, but I think it's better to write this myself.
    # An __init__ function and five properties are not very difficult to get
    # wrong, I think.
    def __init__(self):
        self._address = TypeAddress()
        self._bool = TypeBool()
        self._float = TypeFloat()
        self._int = TypeInt()
        self._string = TypeString()

    @property
    def address(self):
        return self._address

    @property
    def bool(self):
        return self._bool

    @property
    def float(self):
        return self._float

    @property
    def int(self):
        return self._int

    @property
    def string(self):
        return self._string

    def call_relevant(self, type_: str):
        type_ = type_.upper()
        if type_ == "ADDRESS":
            return self._address
        elif type_ == "BOOL":
            return self._bool
        elif type_ == "FLOAT":
            return self._float
        elif type_ == "INT":
            return self._int
        elif type_ == "STRING":
            return self._string
