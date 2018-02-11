import json
import pytest

from django.urls import reverse

from yoflow.flow import Flow
from yoflow import exceptions, views


def test_init(example_parent_flow):
    assert example_parent_flow.reversed_states == {'draft': 1, 'approved': 2, 'final': 3}
    assert example_parent_flow.field == Flow.DEFAULT_FIELD
    assert example_parent_flow.lookup_field == Flow.DEFAULT_LOOKUP_FIELD
    assert example_parent_flow.url_regex == Flow.DEFAULT_URL_REGEX


def test_init_overrides(example_child_flow):
    assert example_child_flow.reversed_states == {'draft': 1, 'approved': 2, 'final': 3}
    assert example_child_flow.field == 'custom_state_field'
    assert example_child_flow.lookup_field == 'uuid'
    assert example_child_flow.url_regex == '<str:uuid>'


def test_basic_flow_urls(example_parent_flow):
    urls = example_parent_flow.urls[0]
    assert len(urls) == 4
    assert urls[0].name == 'history'
    assert urls[1].name == 'draft'
    assert urls[2].name == 'approved'
    assert urls[3].name == 'final'


def test_flow_with_create_urls(example_child_flow):
    urls = example_child_flow.urls[0]
    assert len(urls) == 5
    assert urls[0].name == 'history'
    assert urls[1].name == 'draft'
    assert urls[2].name == 'approved'
    assert urls[3].name == 'final'
    assert urls[4].name == 'create'


# @pytest.mark.django_db
# @pytest.mark.parametrize('user_fixture, result', [
#     ('draft_permission_user', False),
#     ('approved_permission_user', False),
#     ('admin_user', False),
# ])
# def test_create_instance(request, rf, example_parent_flow, user_fixture, result):
#     req = rf.post('/draft')
#     req.user = request.getfuncargvalue(user_fixture)
#     with pytest.raises(exceptions.FlowException):
#         response = views.create(req, example_parent_flow)


def test_process_state_to_state():
    pass

def test_process_on_state():
    pass

def test_process_on_all():
    pass

def test_process():
    pass

def test_check_user_permissions():
    pass
