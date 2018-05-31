from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db import transaction


class Transition(object):

    def __init__(self, obj, transitions, states, state_field='state'):
        self.obj = obj
        self.from_state = getattr(obj, state_field)
        self.states = states
        self.state_field = state_field
        self.transitions = transitions

    @property
    def valid_states(self):
        return self.transitions[self.from_state]

    @staticmethod
    def get_user(request):
        user = request.user
        is_anonymous = user.is_anonymous if isinstance(user.is_anonymous, bool) else user.is_anonymous()
        return None if is_anonymous else user

    def update_state(self, to_state):
        if to_state not in self.valid_states:
            raise PermissionDenied('{} not in allowed states'.format(self.states[to_state]))
        setattr(self.obj, self.state_field, to_state)

    def create_history(self, to_state, meta, request):
        if hasattr(self.obj, 'yoflow_history'):
            if meta is not None and not isinstance(meta, dict):
                error_class = getattr(settings, 'YOFLOW_TYPE_ERROR', TypeError)
                raise error_class('Meta data must be valid JSON object')
            self.obj.yoflow_history.create(
                previous_state=self.states[self.from_state],
                new_state=self.states[to_state],
                meta=meta,
                user=self.get_user(request),
            )

    @transaction.atomic
    def transition(self, to_state, request, meta=None):
        self.update_state(to_state=to_state)
        self.obj.save()
        self.create_history(to_state=to_state, meta=meta, request=request)
