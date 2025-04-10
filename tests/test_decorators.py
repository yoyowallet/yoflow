import pytest

from yoflow.decorators import transition
from yoflow.flow import Flow


class TestView:
    flow = Flow
    request = None

    def get_object(self):
        pass

    @transition(to_state="test")
    def view(self):
        pass


def test_validate(mocker):
    mocked_process = mocker.patch.object(Flow, "process")
    mocker.patch.object(Flow, "validate")
    mocked_validate = mocker.patch.object(Flow, "check_permissions")
    TestView().view()
    assert mocked_validate.call_count == 1
    assert mocked_process.call_count == 1


def test_validate_exception(mocker):
    mocked_process = mocker.patch.object(Flow, "process")
    mocked_validate = mocker.patch.object(Flow, "validate")
    mocked_validate = mocker.patch.object(Flow, "check_permissions")
    mocked_validate.side_effect = Exception

    with pytest.raises(Exception):  # noqa: B017
        TestView().view()

    assert mocked_process.call_count == 0
