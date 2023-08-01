from scripted_video.qualms._root_pseudo_error import RootPseudoError


class BaseQualm(RootPseudoError):
    type: str = "qualm"


class UnrecognizedSyntax(BaseQualm):
    base_msg: str = "Unrecognized syntax: \'{command}\'"

    def __init__(self, command):
        super().__init__()
        self.msg = self.base_msg.format(command=command)

    @classmethod
    def check(cls, node, qualm_group):
        qualm_group.add_qualm(cls(node.contents))
