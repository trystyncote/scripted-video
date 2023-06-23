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
