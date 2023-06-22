import src.scripted_video.syntax as syntax


def match_Declare(node):
    match node:
        case syntax.Declare(name="abc", value="def", type="ghi"):
            assert True
        case _:
            assert False


def match_Doctype(node):
    match node:
        case syntax.Doctype(doctype="scripted-video"):
            assert True
        case _:
            assert False


def match_Metadata(node):
    match node:
        case syntax.Metadata(name="window_width", value="852"):
            assert True
        case _:
            assert False
