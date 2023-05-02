from scripted_video.variables.Metadata import Metadata
from scripted_video.variables.Constants import ConstantVariables


class ScriptVariables:
    def __init__(self):
        self._metadata = Metadata()
        self._constants = ConstantVariables()

    @property
    def metadata(self):
        return self._metadata

    @property
    def constants(self):
        return self._constants
