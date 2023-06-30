class Metadata:
    def __init__(self):
        self._script_file = None
        # The variables below are allowed to be overwritten by being in the
        # public interface.
        self.file_name = None
        self.frame_rate = None
        self.window_height = None
        self.window_width = None

    @property
    def script_file(self):
        return self._script_file

    @script_file.setter
    def script_file(self, val):
        if not self._script_file:
            self._script_file = val
        else:
            raise AttributeError(f"{self.__class__.__name__}: Item is immutable.")

    def update_value(self, key, value):
        self.__setattr__(key, value)
