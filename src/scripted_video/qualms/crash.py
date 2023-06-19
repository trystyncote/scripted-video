from src.scripted_video.qualms._root_pseudo_error import RootPseudoError

import src.scripted_video.syntax as syntax


class BaseCrash(RootPseudoError):
    type: str = "crash"


class DoctypeNotAtBeginning(BaseCrash):
    msg: str = "Doctype declaration did not occur at the beginning of the file."

    @classmethod
    def check(cls, node, qualm_group):
        match node:
            case syntax.TimelineModule(
                body=[
                    syntax.Doctype(doctype="scripted-video"),
                    *_
                ]
            ):
                return
            case _:
                qualm_group.add_qualm(cls())
