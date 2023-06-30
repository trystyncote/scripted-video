from scripted_video.qualms._root_pseudo_error import RootPseudoError


class BaseIssue(RootPseudoError):
    type: str = "issue"
