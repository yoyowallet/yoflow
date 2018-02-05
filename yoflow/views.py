from django.db import transaction
from django.views.decorators.http import require_http_methods

from yoflow import exceptions


def get_object(flow, value):
    return flow.model.objects.get(**{flow.lookup_field: value})


def yoflow(f):
    """
    Call custom authentication logic for view
    Catches all exceptions raising yoflow exception which can be handled by middleware
    """
    def wrapper(request, flow, *args, **kwargs):
        try:
            flow.authenticate(request)
            return f(request, flow, *args, **kwargs)
        except Exception as e:
            raise e if isinstance(e, exceptions.FlowException) else exceptions.FlowException
    return wrapper


@require_http_methods(['PUT'])
@transaction.atomic
@yoflow
def create(request, flow, **kwargs):
    default = flow.model._meta.get_field(flow.field).get_default()
    state = flow.states[default]
    flow.check_user_permissions(user=request.user, new_state=state)
    obj = flow.process_new(request=request)
    return flow.response(obj=obj)


@require_http_methods(['POST'])
@transaction.atomic
@yoflow
def view(request, flow, **kwargs):
    state = request.path.strip('/').split('/')[-1]
    new_state_name = flow.reversed_states[state]
    obj = get_object(flow, kwargs[flow.lookup_field])
    flow.check_user_permissions(user=request.user, new_state=state)
    flow.validate_state_change(obj=obj, new_state=new_state_name)
    flow.process(obj=obj, new_state=state, request=request)
    setattr(obj, flow.field, new_state_name)
    obj.save()
    return flow.response(obj=obj)


@require_http_methods(['GET'])
@yoflow
def history(request, flow, **kwargs):
    obj = get_object(flow, kwargs[flow.lookup_field])
    return flow.response_history(obj.yoflow_history.all())
