import pytest

from yoflow.flow import Flow
from example import flows
from tests import factories


@pytest.fixture
def flow():
    yield flows.PostFlow()


@pytest.fixture
def user_client(client, django_user_model, user):
    user.set_password(user)
    user.save()
    response = client.login(username=user.username, password=user.username)
    yield client


@pytest.mark.django_db
@pytest.fixture
def draft_post():
    yield factories.DraftPostFactory()


@pytest.mark.django_db
@pytest.fixture
def approved_post():
    yield factories.ApprovedPostFactory()
