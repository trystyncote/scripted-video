import src.scripted_video.syntax as syntax


def match_Create(node, exp):
    match node:
        case syntax.Create(
            body=[
                syntax.Property(name=exp.p_name_A, value=exp.p_value_A),
                syntax.Property(name=exp.p_name_B, value=exp.p_value_B)
            ],
            subjects=[syntax.Object(name=exp.o_name)]
        ):
            assert True
        case _:
            assert False


def match_Declare(node, exp):
    match node:
        case syntax.Declare(name=exp.name, value=exp.value, type=exp.type):
            assert True
        case _:
            assert False


def match_Delete(node, exp):
    match node:
        case syntax.Delete(
            body=[syntax.Property(name="delete-time", value=exp.p_value)],
            subjects=[syntax.Object(name=exp.o_name)]
        ):
            assert True
        case _:
            assert False


def match_Doctype(node, exp):
    match node:
        case syntax.Doctype(doctype=exp.doc):
            assert True
        case _:
            assert False


def match_Metadata(node, exp):
    match node:
        case syntax.Metadata(name=exp.name, value=exp.value):
            assert True
        case _:
            assert False


def match_Move(node, exp):
    match node:
        case syntax.Move(
            body=[
                syntax.Property(name="time", value=exp.p_value_A),
                syntax.Property(name="x", value=exp.p_value_B),
                syntax.Property(name="y", value=exp.p_value_C),
                syntax.Property(name="scale", value=exp.p_value_D),
                syntax.Property(name="rate", value=exp.p_value_E)
            ],
            subjects=[syntax.Object(name=exp.o_name)]
        ):
            assert True
        case _:
            assert False
