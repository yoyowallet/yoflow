from django.http import JsonResponse
from rest_framework.exceptions import ValidationError
from yoflow import exceptions, flow
from example import models, serializers


class ParentFlow(flow.Flow):
    model = models.Parent
    states = dict(models.STATES)
    field = 'state'
    lookup_field = 'pk'
    transitions = {
        models.DRAFT: [models.DRAFT, models.APPROVED],
        models.APPROVED: [],
    }

    def response(self, **kwargs):
        return None


class ExampleFlow(flow.Flow):
    """
    Example instances can only be approved when their parent is approved.
    """
    model = models.Example
    states = dict(models.STATES)
    transitions = {
        models.DRAFT: [models.DRAFT, models.APPROVED],
        models.APPROVED: [],
    }

    def draft_to_approved(self, new_state, obj, request, meta, via_admin):
        # {current_state}_to_{new_state} - allows for fine grain state changes
        pass

    def on_draft(self, new_state, obj, request, meta, via_admin):
        # on_{new_state} - catches all changes to new state
        return {'comment': 'I am sending this to draft!'}

    def on_approved(self, new_state, obj, request, meta, via_admin):
        if obj.parent.state != models.APPROVED:
            # check that parent is approved otherwise raise error
            raise ValidationError('Unable to approve because parent is not approved - approve parent first.')

    def on_all(self, new_state, obj, request, meta, via_admin):
        # on_all - catch all state updates
        pass

    def response(self, new_state, obj, request, via_admin):
        serializer = serializers.ExampleSerializer(obj)
        return JsonResponse(serializer.data)
