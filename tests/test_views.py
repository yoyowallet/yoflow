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


mapping = {
    'draft': factories.DraftParentFactory,
    'approved': factories.ApprovedParentFactory,
    'final': factories.FinalParentFactory,
}


@pytest.mark.parametrize("current,new_state,valid", [
    ('draft', 'draft', True),
    ('draft', 'approved', True),
    ('draft', 'final', False),
    ('approved', 'draft', False),
    ('approved', 'approved', True),
    ('approved', 'final', True),
    ('final', 'draft', False),
    ('final', 'approved', False),
    ('final', 'final', True),
])
def test_state_transitions(admin_client, current, new_state, valid):
    obj = mapping[current]()
    uri = '/example/parent/{pk}/{state}/'.format(pk=obj.pk, state=new_state)
    response = admin_client.post(uri, b'{}', content_type='application/json')
    if valid:
        assert response.status_code == 200
    else:
        assert response.status_code == 405
        content = json.loads(response.content)
        assert content['success'] == False
        assert content['message'] == 'Invalid state change from {} to {}'.format(current, new_state)


def test_bad_process():
    pass


def test_obj_state_updated():
    pass


def test_instance_history():
    pass
