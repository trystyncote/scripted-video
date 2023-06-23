from src.scripted_video.objects._time import TIME, _manage_time


class RootInstruction:
    __slots__ = ("_bound_object", "_frame_rate")

    _bound_object: str
    _frame_rate: int

    def __init__(self, bound_object: str, frame_rate: int):
        self._bound_object = bound_object
        self._frame_rate = frame_rate

    @property
    def bound_object(self):
        return self._bound_object

    def confirm_all_attributes_exists(self) -> bool:
        for attr in self.__slots__:
            if getattr(self, attr, None) is None:
                return False
        return True

    def set_attribute(self, name: str, value: str):
        value = self.validate_attribute(name, value)
        self.__setattr__(name, value)

    def validate_attribute(self, name, value):
        annotation = self.__annotations__[name]
        if annotation == TIME:
            value = _manage_time(value, self._frame_rate)
        else:
            value = annotation(value)
        return value


class MoveInstruction(RootInstruction):
    __slots__ = ("rate", "scale", "time", "x", "y")

    rate: TIME
    scale: float
    time: TIME
    x: int
    y: int

    def __init__(self, bound_object: str, frame_rate: int):
        super().__init__(bound_object, frame_rate)

        self.scale = 0.0
        self.x = 0
        self.y = 0
