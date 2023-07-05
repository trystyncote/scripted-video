from pathlib import Path


class ParentType:
    def __setattr__(self, key, value):
        value = self.validate(value)
        super().__setattr__(key, value)

    def create_variable(self, key, value):
        self.__setattr__(key, value)

    def get_variable(self, key):
        return getattr(self, key)

    def validate(self, val):
        raise NotImplementedError


class TypeAddress(ParentType):
    def validate(self, value: (Path | str)) -> Path:
        if isinstance(value, Path):
            return value
        elif isinstance(value, str):
            return Path(value)
        else:
            raise AttributeError(f"{self.__class__.__name__}: Mismatched type.")


class TypeBool(ParentType):
    def validate(self, value: str) -> bool:
        value = value.upper()
        if value == "TRUE":
            return True
        elif value == "FALSE":
            return False
        else:
            raise AttributeError(f"{self.__class__.__name__}: Mismatched type.")


class TypeFloat(ParentType):
    def validate(self, value: (int | float)) -> float:
        if isinstance(value, (int, float)):
            return float(value)
        else:
            raise AttributeError(f"{self.__class__.__name__}: Mismatched type.")


class TypeInt(ParentType):
    def validate(self, value: int) -> int:
        if isinstance(value, int):
            return value
        else:
            raise AttributeError(f"{self.__class__.__name__}: Mismatched type.")


class TypeString(ParentType):
    def validate(self, value: str) -> str:
        if isinstance(value, str):
            return value
        else:
            raise AttributeError(f"{self.__class__.__name__}: Mismatched type.")
