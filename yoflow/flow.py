import json

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.urls import path

from yoflow.views import create, history, view
from yoflow.exceptions import InvalidTransition, PermissionDenied


class Flow(object):

    def __init__(self):
        self.reversed_states = {v: k for k, v in self.states.items()}
        self.field = self.field if hasattr(self, 'field') else 'state'
        self.lookup_field = self.lookup_field if hasattr(self, 'lookup_field') else 'pk'
        self.url_regex = self.url_regex if hasattr(self, 'url_regex') else '<int:pk>'
        self.create_endpoint = True if hasattr(self, 'create') else False

    @property
    def urls(self):
        states = dict(self.states).values()
        urlpatterns = [
            path('{}/history/'.format(self.url_regex), history, {'flow': self}, name='history'),
        ]
        urlpatterns += [
            path('{}/{}/'.format(self.url_regex, state), view, {'flow': self}, name=state) for state in states
        ]
        if self.create_endpoint:
            urlpatterns += [
                path('', create, {'flow': self}, name='create'),
            ]
        return urlpatterns, 'yoflow', self.model._meta.app_label

    def validate_state_change(self, obj, new_state):
        current_state = getattr(obj, self.field)
        if new_state not in self.transitions.get(current_state, []) and current_state != new_state:
            raise InvalidTransition('Invalid state change from {} to {}'.format(
                self.states[current_state],
                self.states[new_state],
            ))

    def process_state_to_state(self, current_state, new_state, meta, **kwargs):
        state_to_state = '{}_to_{}'.format(current_state, new_state)
        if hasattr(self, state_to_state):
            getattr(self, state_to_state)(new_state=new_state, meta=meta, **kwargs)

    def process_on_state(self, new_state, meta, **kwargs):
        on_state = 'on_{}'.format(new_state)
        if hasattr(self, on_state):
            getattr(self, on_state)(new_state=new_state, meta=meta, **kwargs)

    def all(self, meta, **kwargs):
        pass

    def process_new(self, request, obj=None):
        """
        Create new instance of flow model - not supported via admin
        """
        meta = {}
        obj = self.model()
        data = json.loads(request.body) if request.body else None
        self.create(obj=obj, meta=meta, request=request, json=data)
        obj.save()
        if hasattr(obj, 'yoflow_history'):
            obj.yoflow_history.create(
                previous_state=None,
                new_state=obj.get_state_display(),
                meta=meta,
                user=request.user if request.user.is_anonymous is not True else None,
            )
        return obj

    def process(self, obj, new_state, request, via_admin=False):
        current_state = self.states[getattr(obj, self.field)]
        meta = {}
        kwargs = {
            'new_state': new_state,
            'state_changed': current_state != new_state,
            'obj': obj,
            'request': request,
            'via_admin': via_admin,
            'json': json.loads(request.body) if not via_admin and request.body else None,
        }
        self.process_state_to_state(current_state=current_state, meta=meta, **kwargs)
        self.process_on_state(meta=meta, **kwargs)
        self.all(meta=meta, **kwargs)
        if hasattr(obj, 'yoflow_history'):
            obj.yoflow_history.create(
                previous_state=current_state,
                new_state=new_state,
                meta=meta,
                user=request.user if request.user.is_anonymous is not True else None,
            )

    def response(self, obj):
        return JsonResponse({})

    def response_history(self, queryset):
        return JsonResponse(
            list(queryset.values('created_at', 'previous_state', 'new_state', 'user', 'meta')),
            safe=False,
        )

    def check_user_permissions(self, user, new_state):
        try:
            content_type = ContentType.objects.get_for_model(self.model)
            permission = Permission.objects.get(content_type=content_type, codename=new_state)
            if not user.has_perm(permission):
                raise PermissionDenied
        except Permission.DoesNotExist:
            return

    def authenticate(self, request):
        if not request.user.is_authenticated:
            raise PermissionDenied('User not authenticated')

    def to_json(self, request):
        return json.loads(request.body)
