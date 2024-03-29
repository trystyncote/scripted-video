from scripted_video.qualms._root_pseudo_error import RootPseudoError

import scripted_video.svst as svst


class BaseCrash(RootPseudoError):
    type: str = "crash"


class DoctypeNotAtBeginning(BaseCrash):
    msg: str = "Doctype declaration did not occur at the beginning of the file."

    @classmethod
    def check(cls, node, qualm_group):
        match node:
            case svst.TimelineModule(
                body=[
                    svst.Doctype(doctype="scripted-video"),
                    *_
                ]
            ):
                return
            case _:
                qualm_group.add_qualm(cls())
