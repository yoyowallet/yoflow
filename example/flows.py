from django.http import JsonResponse
from rest_framework.exceptions import ValidationError
from yoflow import exceptions, flow
from example import models, permissions, serializers


class ParentFlow(flow.Flow):
    """
    Simplest possible flow - define model, states, and transitions
    """
    model = models.Parent
    states = dict(models.STATES)
    permissions = permissions.ParentPermissions
    transitions = {
        models.DRAFT: [models.APPROVED],
        models.APPROVED: [models.FINAL],
        models.FINAL: [],
    }

    @classmethod
    def create(cls, validated_data, **kwargs):
        return cls.model(name=validated_data['name'])


class ChildFlow(flow.Flow):
    """
    models.Child instances can only be approved when their parent is approved
    models.Child defines a custom uuid primary key & state field so we override defaults
    """
    model = models.Child
    states = dict(models.STATES)
    transitions = {
        models.DRAFT: [models.APPROVED],
        models.APPROVED: [models.FINAL],
        models.FINAL: [],
    }
    state_field = 'custom_state_field'
    url_regex = '(?P<uuid>[0-9a-f-]+)'
    lookup_field = 'uuid'

    @classmethod
    def create(cls, validated_data, **kwargs):
        return cls.model(parent_id=validated_data['parent'])

    @staticmethod
    def draft_to_approved(new_state, obj, request, meta, via_admin):
        meta['comment'] = 'comment'

    @staticmethod
    def on_approved(new_state, obj, request, meta, via_admin):
        if obj.parent.state != models.APPROVED:
            # check that parent is approved otherwise raise error
            raise ValidationError('Unable to approve because parent is not approved - approve parent first.')

    @staticmethod
    def all(meta, **kwargs):
        meta['all'] = 'all'

    @staticmethod
    def response(obj):
        serializer = serializers.ChildSerializer(obj)
        return JsonResponse(serializer.data)
