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
    url_regex = '<str:uuid>'
    lookup_field = 'uuid'

    def draft_to_approved(self, new_state, obj, request, meta, via_admin):
        return {'comment': 'I am approving this!'}

    def on_approved(self, new_state, obj, request, meta, via_admin):
        if obj.parent.state != models.APPROVED:
            # check that parent is approved otherwise raise error
            raise ValidationError('Unable to approve because parent is not approved - approve parent first.')

    def response(self, obj):
        serializer = serializers.ExampleSerializer(obj)
        return JsonResponse(serializer.data)

    def authenticate(self, request):
        # no auth for example - not recommended
        pass

    def check_user_permissions(self, user, new_state):
        # no permission check for example - not recommended
        pass
