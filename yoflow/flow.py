from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.urls import path

from yoflow.views import view
from yoflow.exceptions import FlowException


class Flow(object):

    def __init__(self):
        self.reversed_states = {v: k for k, v in self.states.items()}
        self.field = self.field if hasattr(self, 'field') else 'state'
        self.lookup_field = self.lookup_field if hasattr(self, 'lookup_field') else 'pk'

    @property
    def urls(self):
        states = dict(self.states).values()
        urlpatterns = [
            path('{}/'.format(state), view, {'flow': self}, name=state) for state in states
        ]
        return urlpatterns, 'yoflow', 'yoflow'

    def validate_state_change(self, current_state, new_state):
        if new_state not in self.transitions.get(current_state, []):
            raise FlowException('Invalid state change from "{}" to "{}"'.format(
                self.states[current_state],
                self.states[new_state],
            ))

    def process_state_to_state(self, current_state, new_state, **kwargs):
        state_to_state = '{}_to_{}'.format(current_state, new_state)
        return getattr(self, state_to_state)(**kwargs) if hasattr(self, state_to_state) else kwargs['response']

    def process_on_state(self, new_state, **kwargs):
        on_state = 'on_{}'.format(new_state)
        return getattr(self, on_state)(**kwargs) if hasattr(self, on_state) else kwargs['response']

    def process_on_all(self, **kwargs):
        on_all = 'on_all'
        return getattr(self, on_all)(**kwargs) if hasattr(self, on_all) else kwargs['response']

    def process(self, obj, current_state, new_state, request=None, via_admin=False):
        kwargs = {
            'request': request,
            'response': {},
            'obj': obj,
            'via_admin': via_admin,
        }
        response = self.process_state_to_state(current_state, new_state, **kwargs)
        response = self.process_on_state(new_state, **kwargs)
        response = self.process_on_all(**kwargs)
        return response

    def check_user_permissions(self, user, new_state):
        try:
            content_type = ContentType.objects.get_for_model(self.model)
            permission = Permission.objects.get(content_type=content_type, codename=new_state)
            if not user.has_perm(permission):
                raise PermissionDenied()
        except Permission.DoesNotExist:
            return
