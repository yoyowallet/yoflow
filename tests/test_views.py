import json
import pytest

from django.conf import settings
from django.test import override_settings
from rest_framework import status
from rest_framework.exceptions import APIException

from example import views

urls = [
    ('/blog/post/{}/approved/'),
    ('/blog/post-view/{}/approved/'),
    ('/blog/post-cbv/{}/approved/'),
]


@pytest.mark.django_db
@pytest.mark.parametrize('url', urls)
def test_approved(admin_client, draft_post, url):
    response = admin_client.post(url.format(draft_post.id))
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
@pytest.mark.parametrize('url', urls)
def test_approved_meta(admin_client, draft_post, url):
    meta = {'valid': 'jsonobj'}
    response = admin_client.post(
        url.format(draft_post.id),
        json.dumps(meta),
        content_type='application/json',
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_approved_bad_meta(admin_client, draft_post):
    with override_settings():
        del settings.YOFLOW_TYPE_ERROR
        meta = 'bad'
        with pytest.raises(TypeError):
            response = admin_client.post(
                '/blog/post/{}/approved/'.format(draft_post.id),
                json.dumps(meta),
                content_type='application/json',
            )


@pytest.mark.django_db
def test_approved_bad_meta_override(admin_client, draft_post):
    meta = 'bad'
    response = admin_client.post(
        '/blog/post/{}/approved/'.format(draft_post.id),
        json.dumps(meta),
        content_type='application/json',
    )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
