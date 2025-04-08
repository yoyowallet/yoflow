from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db import transaction

from yoflow.transition import Transition


class Flow:
    @property
    def field(self):
        if hasattr(self, "state_field"):
            return self.state_field
        return getattr(settings, "YOFLOW_DEFAULT_STATE_FIELD", "state")

    @property
    def states(self):
        return dict(self.model._meta.get_field(self.field).choices)

    def default_process(self, *args, **kwargs):
        pass

    def check_permissions(self, obj, to_state):
        from_state = getattr(obj, self.field)
        valid_states = self.transitions[from_state]
        if to_state not in valid_states:
            raise PermissionDenied(f"{self.states[to_state]} not in allowed states")

    def process_state_to_state(self, from_state, to_state, obj, meta):
        state_to_state = f"{from_state}_to_{to_state}"
        getattr(self, state_to_state, self.default_process)(obj=obj, meta=meta)

    def process_on_state(self, to_state, obj, meta):
        on_state = f"on_{to_state}"
        getattr(self, on_state, self.default_process)(obj=obj, meta=meta)

    def process_all(self, obj, meta):
        getattr(self, "all", self.default_process)(obj=obj, meta=meta)

    def validate(self, view):
        """
        Override to run preprocessing validation checks -
        e.g. raise exception if POST body invalid
        :return: meta json
        """
        pass

    @transaction.atomic
    def process(self, obj, to_state, request, meta=None):
        from_state = getattr(obj, self.field)
        transition = Transition(obj=obj, state_field=self.field, from_state=from_state, states=self.states)
        transition.transition(to_state=to_state, meta=meta, request=request)
        # process custom state update logic
        self.process_state_to_state(
            from_state=self.states[from_state],
            to_state=self.states[to_state],
            obj=obj,
            meta=meta,
        )
        self.process_on_state(to_state=self.states[to_state], obj=obj, meta=meta)
        self.process_all(obj=obj, meta=meta)
