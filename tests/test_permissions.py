import pytest

from django.contrib.auth.models import AnonymousUser

from yoflow.permissions import Permissions


@pytest.fixture(scope='session')
def permissions():
    return Permissions()


@pytest.fixture
def anonymous_request(rf):
    request = rf.get('')
    request.user = AnonymousUser()
    yield request


@pytest.fixture
def admin_user_request(admin_user, rf):
    request = rf.get('')
    request.user = admin_user
    yield request


@pytest.fixture(params=['anonymous_request', 'admin_user_request'])
def requests(request):
    return request.getfuncargvalue(request.param)


def test_default_authenticate_permission_anonymous_user(anonymous_request, permissions):
    assert not permissions.authenticate(request=anonymous_request)


def test_default_authenticate_permission_user(admin_user_request, permissions):
    assert permissions.authenticate(request=admin_user_request)


def test_default_can_create_permission_user(requests, permissions):
    assert not permissions.can_create(request=requests)


def test_default_can_delete_permission_user(requests, permissions):
    assert not permissions.can_delete(request=requests, obj=None)


def test_default_can_view_history_permission_user(requests, permissions):
    assert not permissions.can_view_history(request=requests, obj=None)
