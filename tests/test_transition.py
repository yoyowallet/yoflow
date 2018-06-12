import json
import pytest

from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.test import override_settings
from django.test.client import RequestFactory
from rest_framework.exceptions import APIException
from yoflow.transition import Transition

from example import models


@pytest.fixture
def transition(draft_post, flow):
    yield Transition(
        obj=draft_post,
        transitions=flow.transitions,
        states=dict(models.Post.STATES),
        state_field=flow.field,
    )


@pytest.mark.django_db
def test_valid_states(transition):
    assert transition.valid_states == [models.Post.APPROVED]


def test_get_user_fallback(rf):
    request = rf.request()
    request.user = AnonymousUser()
    user = Transition.get_user(request=request)
    assert user is None


@pytest.mark.django_db
def test_get_user(rf):
    request = rf.request()
    test_user = User.objects.create_user(username='test', email='test@example.com', password='top_secret')
    request.user = test_user
    user = Transition.get_user(request=request)
    assert user == test_user


@pytest.mark.django_db
def test_update_state(transition):
    transition.update_state(to_state=models.Post.APPROVED)
    assert transition.obj.state == models.Post.APPROVED


@pytest.mark.django_db
def test_create_history(transition, rf):
    request = rf.request()
    request.user = AnonymousUser()
    transition.create_history(to_state=models.Post.APPROVED, request=request, meta=None)
    assert transition.obj.yoflow_history.count() == 1


@pytest.mark.django_db
def test_create_history_meta_valid_json_object(transition, rf):
    request = rf.request()
    request.user = AnonymousUser()
    data = { 'test': True }
    transition.create_history(to_state=models.Post.APPROVED, request=request, meta=data)
    assert transition.obj.yoflow_history.count() == 1
    assert transition.obj.yoflow_history.first().meta == data


@pytest.mark.django_db
@pytest.mark.parametrize("data", [
    'test',
    1,
    [1, 2],
    True,
    False,
])
def test_create_history_meta_invalid_json_objects(transition, rf, data):
    with override_settings():
        del settings.YOFLOW_TYPE_ERROR
        request = rf.request()
        request.user = AnonymousUser()
        request.data = data
        with pytest.raises(TypeError):
            transition.create_history(to_state=models.Post.APPROVED, request=request)


@pytest.mark.django_db
def test_transition(transition, mocker, rf):
    request = rf.request()
    request.user = AnonymousUser()
    transition.transition(to_state=models.Post.APPROVED, request=request)
    obj = models.Post.objects.get(pk=transition.obj.pk)
    assert obj.state == models.Post.APPROVED
    assert obj.yoflow_history.count() == 1


@pytest.mark.django_db
def test_transition_atomic_update_state(transition, mocker, rf):
    request = rf.request()
    mocked = mocker.patch.object(transition, 'update_state')
    mocked.side_effect = mocker.Mock(side_effect=Exception())
    with pytest.raises(Exception):
        transition.transition(to_state=models.Post.APPROVED, request=request)

    obj = models.Post.objects.get(pk=transition.obj.pk)
    assert obj.state == models.Post.DRAFT
    assert obj.yoflow_history.count() == 0


@pytest.mark.django_db
def test_transition_atomic_create_history(transition, mocker):
    mocked = mocker.patch.object(transition, 'create_history')
    mocked.side_effect = mocker.Mock(side_effect=Exception())
    with pytest.raises(Exception):
        transition.transition(to_state=models.Post.APPROVED, request=mocker.Mock())

    obj = models.Post.objects.get(pk=transition.obj.pk)
    assert obj.state == models.Post.DRAFT
    assert obj.yoflow_history.count() == 0
