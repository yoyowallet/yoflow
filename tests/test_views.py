import json
import pytest

from django.test.utils import override_settings

from yoflow import exceptions, views
from tests import factories


def test_create_instance_not_supported(rf, example_parent_flow, user):
    request = rf.post('/example/parent/draft/')
    request.user = user
    with pytest.raises(exceptions.FlowException):
        response = views.create(request, example_parent_flow)


@pytest.mark.django_db
def test_create_instance_supported(rf, example_parent_flow, user):
    payload = json.dumps({'name': 'parent'})
    request = rf.post('/example/parent/', payload, content_type='application/json')
    request.user = user
    response = views.create(request, example_parent_flow)


def test_bad_state(rf, example_parent_flow, user):
    request = rf.post('/example/parent/1/unknown-state/')
    request.user = user
    with pytest.raises(exceptions.FlowException):
        response = views.create(request, example_parent_flow)


def test_bad_state_response(user_client, example_parent_flow):
    response = user_client.post('/example/parent/1/unknown-state/')
    assert response.status_code == 404


def test_object_not_found(user, rf, example_parent_flow):
    request = rf.post('/example/parent/1/draft/')
    request.user = user
    with pytest.raises(exceptions.FlowException):
        response = views.update(request, example_parent_flow, pk=1)


def test_object_not_found_response(user_client, example_parent_flow):
    response = user_client.post('/example/parent/1/draft/')
    assert response.status_code == 404
    assert json.loads(response.content)['success'] == False


def test_bad_permission():
    pass


@pytest.mark.parametrize("factory,new_state,valid", [
    (factories.DraftParentFactory, 'draft', True),
    (factories.DraftParentFactory, 'approved', True),
    (factories.DraftParentFactory, 'final', False),
    (factories.ApprovedParentFactory, 'draft', False),
    (factories.ApprovedParentFactory, 'approved', True),
    (factories.ApprovedParentFactory, 'final', True),
    (factories.FinalParentFactory, 'draft', False),
    (factories.FinalParentFactory, 'approved', False),
    (factories.FinalParentFactory, 'final', True),
])
def test_state_transitions(admin_client, factory, new_state, valid):
    obj = factory()
    uri = '/example/parent/{pk}/{state}/'.format(pk=obj.pk, state=new_state)
    response = admin_client.post(uri, b'{}', content_type='application/json')
    if valid:
        assert response.status_code == 200
    else:
        assert response.status_code == 405
        content = json.loads(response.content)
        assert content['success'] == False
        expeted_messaged = 'Invalid state change from {} to {}'.format(obj.get_state_display(), new_state)
        assert content['message'] == expeted_messaged


def test_bad_process():
    pass


def test_obj_state_updated():
    pass


def test_instance_history():
    pass
