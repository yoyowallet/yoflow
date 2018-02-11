import pytest

from yoflow.flow import Flow
from example import flows, models


@pytest.fixture
def example_parent_flow():
    yield flows.ParentFlow()


@pytest.fixture
def example_child_flow():
    yield flows.ChildFlow()


@pytest.fixture
def draft_permission_user(django_user_model):
    return django_user_model.objects.create(username='draft')


@pytest.fixture
def approved_permission_user(django_user_model):
    return django_user_model.objects.create(username='approved')


@pytest.fixture
def superuser_permission_user(django_user_model):
    return django_user_model.objects.create(username='superuser', is_superuser=True)


@pytest.fixture(params=['draft_permission_user', 'approved_permission_user', 'superuser_permission_user'])
def user(request):
    return request.getfuncargvalue(request.param)


@pytest.fixture
def user_client(client, django_user_model, user):
    user.set_password(user)
    user.save()
    response = client.login(username=user.username, password=user.username)
    yield client


@pytest.mark.django_db
@pytest.fixture
def parent():
    yield models.Parent.objects.create(name='parent')


@pytest.mark.django_db
@pytest.fixture
def child(parent):
    yield models.Child.objects.create(name='child', parent=parent)
