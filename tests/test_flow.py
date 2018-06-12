import json
import pytest

from django.test import override_settings
from django.urls import reverse
from yoflow.flow import Flow

from example import models


def test_state_field_default():
    flow = Flow()
    assert flow.field == 'state'


@override_settings(YOFLOW_DEFAULT_STATE_FIELD='test')
def test_state_field_settings():
    flow = Flow()
    assert flow.field == 'test'


def test_state_field_class():
    field = 'test'
    class Test(Flow):
        state_field = field
    assert Test().field == field


def test_states(flow):
    assert flow.states == dict(models.Post.STATES)


@pytest.fixture
def mock_transition(mocker):
    return mocker.patch('yoflow.flow.Transition')


@pytest.mark.django_db
def test_process_state_to_state(flow, draft_post, mocker, mock_transition):
    mock_state_to_state = mocker.patch.object(flow, 'draft_to_approved')
    flow.process(obj=draft_post, to_state=models.Post.APPROVED, request=mocker.Mock())
    assert mock_state_to_state.call_count == 1


@pytest.mark.django_db
def test_process_on_state(flow, draft_post, mocker, mock_transition):
    mock_on_state = mocker.patch.object(flow, 'on_approved')
    flow.process(obj=draft_post, to_state=models.Post.APPROVED, request=mocker.Mock())
    assert mock_on_state.call_count == 1


@pytest.mark.django_db
def test_process_all(flow, draft_post, mocker, mock_transition):
    mock_all = mocker.patch.object(flow, 'all')
    flow.process(obj=draft_post, to_state=models.Post.APPROVED, request=mocker.Mock())
    assert mock_all.call_count == 1
