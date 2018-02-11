import json
import pytest

from django.test.utils import override_settings

from yoflow import exceptions, views


@pytest.mark.django_db
def test_create_instance_not_supported(rf, example_parent_flow, user):
    request = rf.post('/example/parent/draft/')
    request.user = user
    with pytest.raises(exceptions.FlowException):
        response = views.create(request, example_parent_flow)


@pytest.mark.django_db
def test_create_instance_supported(rf, parent, example_child_flow, user):
    # TODO add permission support and tests for creation
    payload = json.dumps({'parent': parent.pk, 'name': 'child'})
    request = rf.post('/example/child/draft/', payload, content_type='application/json')
    request.user = user
    response = views.create(request, example_child_flow)


def test_bad_state(rf, example_parent_flow, user):
    request = rf.post('/example/parent/1/unknown-state/')
    request.user = user
    with pytest.raises(exceptions.FlowException):
        response = views.create(request, example_parent_flow)


def test_bad_state_response(user_client, example_parent_flow):
    response = user_client.post('/example/parent/1/unknown-state/')
    assert response.status_code == 404 # TODO json response?


def test_object_not_found(user, rf, example_parent_flow):
    request = rf.post('/example/parent/1/draft/')
    request.user = user
    with pytest.raises(exceptions.FlowException):
        response = views.view(request, example_parent_flow, pk=1)


def test_object_not_found_response(user_client, example_parent_flow):
    response = user_client.post('/example/parent/1/draft/')
    assert response.status_code == 404
    assert json.loads(response.content)['success'] == False


def test_bad_permission():
    pass


def test_invalid_state_change_raises_exception(rf, admin_user, example_parent_flow, parent):
    request = rf.post('/example/parent/1/final/')
    request.user = admin_user
    with pytest.raises(exceptions.InvalidTransition):
        response = views.view(request, example_parent_flow, pk=parent.pk)


def test_invalid_state_change_raises_exception_response(admin_client, example_parent_flow, parent):
    response = admin_client.post('/example/parent/{}/final/'.format(parent.pk))
    assert response.status_code == 405
    assert json.loads(response.content)['success'] == False


def test_bad_process():
    pass


def test_obj_state_updated():
    pass


def test_instance_history():
    pass
