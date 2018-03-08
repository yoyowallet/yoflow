import json

from django.http import JsonResponse
from django.conf.urls import url

from yoflow.exceptions import InvalidTransition, PermissionDenied
from yoflow.permissions import Permissions
from yoflow.views import create, delete, history, update


class Flow(object):

    DEFAULT_STATE_FIELD = 'state'
    DEFAULT_LOOKUP_FIELD = 'pk'
    DEFAULT_URL_REGEX = '(?P<pk>\d+)'

    def __init__(self):
        self.reversed_states = {v: k for k, v in self.states.items()}
        self.state_field = self.state_field if hasattr(self, 'state_field') else self.DEFAULT_STATE_FIELD
        self.lookup_field = self.lookup_field if hasattr(self, 'lookup_field') else self.DEFAULT_LOOKUP_FIELD
        self.url_regex = self.url_regex if hasattr(self, 'url_regex') else self.DEFAULT_URL_REGEX
        self.permissions = self.permissions if hasattr(self, 'permissions') else Permissions

    @property
    def urls(self):
        states = dict(self.states).values()
        urlpatterns = [
            url(r'{}/{}/$'.format(self.url_regex, state), update, {'flow': self}, name=state) for state in states
        ]
        urlpatterns += [
            url(r'^$', create, {'flow': self}, name='create'),
            url(r'{}/$'.format(self.url_regex), delete, {'flow': self}, name='delete'),
            url(r'{}/history/$'.format(self.url_regex), history, {'flow': self}, name='history'),
        ]
        return urlpatterns, 'yoflow', '{}:{}'.format(self.model._meta.app_label, str(self.model._meta))

    def validate_state_change(self, current_state, new_state):
        if new_state not in self.transitions.get(current_state, []) and current_state != new_state:
            raise InvalidTransition('Invalid state change from {} to {}'.format(
                self.states[current_state],
                self.states[new_state],
            ))

    def default_process(*args, **kwargs):
        pass

    def process_state_to_state(self, current_state, new_state, meta, **kwargs):
        state_to_state = '{}_to_{}'.format(current_state, new_state)
        getattr(self, state_to_state, self.default_process)(new_state=new_state, meta=meta, **kwargs)

    def process_on_state(self, new_state, meta, **kwargs):
        on_state = 'on_{}'.format(new_state)
        getattr(self, on_state, self.default_process)(new_state=new_state, meta=meta, **kwargs)

    def all(self, meta, **kwargs):
        pass

    @staticmethod
    def _get_user(request):
        user = request.user
        is_anonymous = user.is_anonymous if isinstance(user.is_anonymous, bool) else user.is_anonymous()
        return None if is_anonymous else user

    @staticmethod
    def admin_json(cleaned_data):
        return cleaned_data

    @staticmethod
    def validate_data(data, **kwargs):
        return data

    def validate(self, request, cleaned_data, state, obj=None):
        via_admin = cleaned_data is not None
        data = None
        if via_admin:
            data = self.admin_json(cleaned_data)  # via admin
        elif cleaned_data is None and request.body:
            data = json.loads(request.body)
        return self.validate_data(data=data, request=request, obj=obj, state=state, via_admin=via_admin)

    def process_new(self, request, cleaned_data=None):
        if not hasattr(self, 'create'):
            raise PermissionDenied('Unable to create new {}'.format(self.model._meta))  # TODO test model name with py27

        meta = {}
        default_state = self.model._meta.get_field(self.state_field).default
        validated_data = self.validate(request=request, cleaned_data=cleaned_data, state=default_state)
        obj = self.create(meta=meta, request=request, validated_data=validated_data)
        obj.save()

        if hasattr(obj, 'yoflow_history'):
            obj.yoflow_history.create(
                previous_state=None,
                new_state=getattr(obj, 'get_{}_display'.format(self.state_field))(),
                meta=meta,
                user=self._get_user(request)
            )

        return obj

    def process(self, obj, new_state_name, request, cleaned_data=None):
        obj_state = getattr(obj, self.state_field)
        new_state = self.reversed_states[new_state_name]
        self.validate_state_change(current_state=obj_state, new_state=new_state)
        obj_state_name = self.states[getattr(obj, self.state_field)]

        meta = {}
        kwargs = {
            'new_state': new_state_name,
            'state_changed': obj_state_name != new_state_name,
            'obj': obj,
            'request': request,
            'via_admin': cleaned_data is not None,
            'cleaned_data': cleaned_data,
            'validated_data': self.validate(obj=obj, request=request, cleaned_data=cleaned_data, state=new_state),
        }
        self.process_state_to_state(current_state=obj_state_name, meta=meta, **kwargs)
        self.process_on_state(meta=meta, **kwargs)
        self.all(meta=meta, **kwargs)
        if hasattr(obj, 'yoflow_history'):
            obj.yoflow_history.create(
                previous_state=obj_state_name,
                new_state=new_state_name,
                meta=meta,
                user=self._get_user(request),
            )

    def response(self, obj):
        return JsonResponse({})

    def response_delete(self):
        return JsonResponse({}, status=204)

    def response_history(self, queryset):
        return JsonResponse(
            list(queryset.values('created_at', 'previous_state', 'new_state', 'user', 'meta')),
            safe=False,
        )

    def check_permissions(self, request, obj, new_state_name):
        permission_check = 'has_{}_permission'.format(new_state_name)
        if hasattr(self.permissions, permission_check):
            if not getattr(self.permissions, permission_check)(request=request, obj=obj):
                raise PermissionDenied('Permission denied for {}'.format(new_state_name))
        else:
            raise PermissionDenied('You do not have permission for {} state'.format(new_state_name))

    def to_json(self, request):
        return json.loads(request.body)
