from scripted_video.qualms._root_pseudo_error import RootPseudoError


class BaseQualm(RootPseudoError):
    type: str = "qualm"
