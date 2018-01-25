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

    @classmethod
    def _state_to_state(cls, current_state, new_state):
        return '{}_to_{}'.format(current_state, new_state)

    @classmethod
    def _on_state(cls, new_state):
        return 'on_{}'.format(new_state)

    @classmethod
    def _on_all(cls):
        return 'on_all'

    @classmethod
    def fallback(cls, result):
        return lambda obj, response, request: result

    @classmethod
    def process(cls, obj, current_state, new_state, request=None, via_admin=False):
        response = {}
        kwargs = {
            'request': request,
            'response': response,
            'obj': obj,
            'via_admin': via_admin,
        }
        state_to_state = cls._state_to_state(current_state, new_state)
        if hasattr(cls, state_to_state):
            response = getattr(cls, state_to_state)(**kwargs) or response
        on_state = cls._on_state(new_state)
        if hasattr(cls, on_state):
            response = getattr(cls, on_state)(**kwargs) or response
        if hasattr(cls, 'on_all'):
            response = getattr(cls, 'on_all')(**kwargs) or response
        return response

    def check_user_permissions(self, user):
        # TODO raise exception if check fails
        pass
