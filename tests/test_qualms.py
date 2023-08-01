import scripted_video.qualms as qualms
from scripted_video.qualms.force_exit import svForceExit

import io
import pytest
import sys


@pytest.fixture
def capture_stdout(monkeypatch):
    # See https://github.com/mCodingLLC/SlapThatLikeButton-TestingStarterProject/blob/main/tests/conftest.py
    buffer = {"stdout": "", "write_calls": 0}

    def fake_write(s):
        buffer["stdout"] += s
        buffer["write_calls"] += 1

    monkeypatch.setattr(sys.stdout, 'write', fake_write)
    return buffer


def test_qualms_group_add():
    group = qualms.QualmGroup()
    assert group.has_qualms is False

    group.add_qualm(qualms.BaseQualm())
    assert group.has_qualms is True


def test_qualms_group_add_crash(capture_stdout):
    # capture_stdout is passed in to prevent print side effects.
    group = qualms.QualmGroup()
    with pytest.raises(svForceExit):
        group.add_qualm(qualms.BaseCrash())


@pytest.mark.parametrize("added_qualms,expected_sequence", [
    ((qualms.BaseIssue(), qualms.BaseQualm()),
     (f"+{'-'*37}", "| :group: QualmGroup", f"+-+{'-'*16} 1 {'-'*16}", "  | :issue: BaseIssue", "  |   ",
      f"  +{'-'*16} 2 {'-'*16}", "  | :qualm: BaseQualm", "  |   ", f"  +{'-'*35}"))
])
def test_qualms_group_traceback(added_qualms, expected_sequence, capture_stdout):
    expected = io.StringIO()
    for line in expected_sequence:
        expected.write(f"{line}\n")
    expected = expected.getvalue()

    group = qualms.QualmGroup(*added_qualms)
    group.traceback()
    assert capture_stdout["stdout"] == expected


@pytest.mark.parametrize("qualm_object", [
    qualms.BaseCrash(),
    qualms.BaseIssue(),
    qualms.BaseQualm(),
    qualms.DoctypeNotAtBeginning()
])
def test_qualms_raise(qualm_object, capture_stdout):
    # capture_stdout is passed in to prevent print side effects.
    with pytest.raises(svForceExit):
        qualm_object.raise_qualms()


@pytest.mark.parametrize("qualm_object,expected_sequence", [
    (qualms.BaseCrash(), (":crash: BaseCrash", "  ")),
    (qualms.BaseIssue(), (":issue: BaseIssue", "  ")),
    (qualms.BaseQualm(), (":qualm: BaseQualm", "  ")),
    (qualms.DoctypeNotAtBeginning(),
     (":crash: DoctypeNotAtBeginning", "  Doctype declaration did not occur at the beginning of the file."))
])
def test_qualms_traceback(qualm_object, expected_sequence, capture_stdout):
    expected = io.StringIO()
    for line in expected_sequence:
        expected.write(f"{line}\n")
    expected = expected.getvalue()

    qualm_object.traceback()
    assert capture_stdout["stdout"] == expected
