from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.urls import path

from yoflow.views import history, view
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
            path('history/', history, {'flow': self}, name='history'),
        ]
        urlpatterns += [
            path('{}/'.format(state), view, {'flow': self}, name=state) for state in states
        ]
        return urlpatterns, 'yoflow', 'yoflow'

    def validate_state_change(self, obj, new_state):
        current_state = getattr(obj, self.field)
        if new_state not in self.transitions.get(current_state, []):
            raise FlowException('Invalid state change from "{}" to "{}"'.format(
                self.states[current_state],
                self.states[new_state],
            ))

    def process_state_to_state(self, current_state, new_state, meta, **kwargs):
        state_to_state = '{}_to_{}'.format(current_state, new_state)
        if hasattr(self, state_to_state):
            return getattr(self, state_to_state)(new_state=new_state, meta=meta, **kwargs)

    def process_on_state(self, new_state, meta, **kwargs):
        on_state = 'on_{}'.format(new_state)
        return getattr(self, on_state)(new_state=new_state, meta=meta, **kwargs) if hasattr(self, on_state) else meta

    def all(self, meta, **kwargs):
        return meta

    def process(self, obj, new_state, request, via_admin=False):
        current_state = self.states[getattr(obj, self.field)]
        meta = {}
        kwargs = {
            'new_state': new_state,
            'obj': obj,
            'request': request,
            'via_admin': via_admin,
        }
        meta = self.process_state_to_state(current_state=current_state, meta={}, **kwargs) or meta
        meta = self.process_on_state(meta=meta, **kwargs) or meta
        meta = self.all(meta=meta, **kwargs) or meta
        if hasattr(obj, 'yoflow_history'):
            obj.yoflow_history.create(
                previous_state=current_state,
                new_state=new_state,
                meta=meta,
                user=request.user if request.user.is_anonymous is not True else None,
            )

    def response(self, obj):
        return JSONResponse({})

    def response_history(self, queryset):
        return JSONResponse(
            list(queryset.values('created_at', 'previous_state', 'new_state', 'user', 'meta')),
            safe=False,
        )

    def check_user_permissions(self, user, new_state):
        try:
            content_type = ContentType.objects.get_for_model(self.model)
            permission = Permission.objects.get(content_type=content_type, codename=new_state)
            if not user.has_perm(permission):
                raise PermissionDenied()
        except Permission.DoesNotExist:
            return

    def authenticate(self, request):
        if not request.user.is_authenticated:
            raise PermissionDenied
