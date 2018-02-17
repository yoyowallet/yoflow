from django.db import transaction
from django.views.decorators.http import require_http_methods

from yoflow import exceptions


def get_object(flow, value):
    try:
        return flow.model.objects.get(**{flow.lookup_field: value})
    except flow.model.DoesNotExist:
        raise exceptions.ObjectNotFound


def yoflow(f):
    """
    Call custom authentication logic for view
    Catches all exceptions raising yoflow exception which can be handled by middleware
    """
    def wrapper(request, flow, *args, **kwargs):
        try:
            if not flow.permissions.authenticate(request):
                raise exceptions.PermissionDenied('User not authenticated')
            return f(request, flow, *args, **kwargs)
        except Exception as e:
            raise e if isinstance(e, exceptions.FlowException) else exceptions.FlowException
    return wrapper


@require_http_methods(['POST'])
@transaction.atomic
@yoflow
def create(request, flow, **kwargs):
    default = flow.model._meta.get_field(flow.state_field).get_default()
    state = flow.states[default]
    if not flow.permissions.can_create(request):
        raise PermissionDenied('You do not have permission to create new instances')
    obj = flow.process_new(request=request)
    return flow.response(obj=obj)


@require_http_methods(['DELETE'])
@transaction.atomic
@yoflow
def delete(request, flow, **kwargs):
    if not flow.permissions.can_delete(request):
        raise PermissionDenied('You do not have permission to delete instances')
    obj = get_object(flow, kwargs[flow.lookup_field])
    obj.delete()
    return flow.response_delete()


@require_http_methods(['POST'])
@transaction.atomic
@yoflow
def update(request, flow, **kwargs):
    state = request.path.strip('/').split('/')[-1]
    new_state_id = flow.reversed_states[state]
    obj = get_object(flow, kwargs[flow.lookup_field])
    flow.check_permissions(request=request, new_state=state)
    flow.validate_state_change(obj=obj, new_state=new_state_id)
    flow.process(obj=obj, new_state=state, request=request)
    setattr(obj, flow.state_field, new_state_id)
    obj.save()
    return flow.response(obj=obj)


@require_http_methods(['GET'])
@yoflow
def history(request, flow, **kwargs):
    if not flow.permissions.can_view_history(request):
        raise PermissionDenied('You do not have permission to view instance history')
    obj = get_object(flow, kwargs[flow.lookup_field])
    return flow.response_history(obj.yoflow_history.all())
