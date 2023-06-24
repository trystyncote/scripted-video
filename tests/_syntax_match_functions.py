import src.scripted_video.svst as svst


def match_Create(node, exp):
    match node:
        case svst.Create(
            body=[
                svst.Property(name=exp.p_name_A, value=exp.p_value_A),
                svst.Property(name=exp.p_name_B, value=exp.p_value_B)
            ],
            subjects=[svst.Object(name=exp.o_name)]
        ):
            assert True
        case _:
            assert False


def match_Declare(node, exp):
    match node:
        case svst.Declare(name=exp.name, value=exp.value, type=exp.type):
            assert True
        case _:
            assert False


def match_Delete(node, exp):
    match node:
        case svst.Delete(
            body=[svst.Property(name="delete-time", value=exp.p_value)],
            subjects=[svst.Object(name=exp.o_name)]
        ):
            assert True
        case _:
            assert False


def match_Doctype(node, exp):
    match node:
        case svst.Doctype(doctype=exp.doc):
            assert True
        case _:
            assert False


def match_Metadata(node, exp):
    match node:
        case svst.Metadata(name=exp.name, value=exp.value):
            assert True
        case _:
            assert False


def match_Move(node, exp):
    match node:
        case svst.Move(
            body=[
                svst.Property(name="time", value=exp.p_value_A),
                svst.Property(name="x", value=exp.p_value_B),
                svst.Property(name="y", value=exp.p_value_C),
                svst.Property(name="scale", value=exp.p_value_D),
                svst.Property(name="rate", value=exp.p_value_E)
            ],
            subjects=[svst.Object(name=exp.o_name)]
        ):
            assert True
        case _:
            assert False
