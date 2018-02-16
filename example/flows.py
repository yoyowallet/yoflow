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

    def create(self, obj, json, **kwargs):
        obj.name = json['name']


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
    field = 'custom_state_field'
    url_regex = '<str:uuid>'
    lookup_field = 'uuid'

    def create(self, obj, json, **kwargs):
        obj.parent_id = json['parent']

    def draft_to_approved(self, new_state, obj, request, meta, via_admin):
        return {'comment': 'I am approving this!'}

    def on_approved(self, new_state, obj, request, meta, via_admin):
        if obj.parent.state != models.APPROVED:
            # check that parent is approved otherwise raise error
            raise ValidationError('Unable to approve because parent is not approved - approve parent first.')

    def response(self, obj):
        serializer = serializers.ChildSerializer(obj)
        return JsonResponse(serializer.data)
