from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


def get_object(flow, value):
    return flow.model.objects.get(**{flow.lookup_field: value})


def authenticate(f):
    def wrapper(request, flow, *args, **kwargs):
        flow.authenticate(request)
        return f(request, flow, *args, **kwargs)
    return wrapper


@require_http_methods(['POST'])
@transaction.atomic
@authenticate
def view(request, flow, **kwargs):
    flow.authenticate(request)
    state = request.path.strip('/').split('/')[-1]
    new_state_name = flow.reversed_states[state]
    obj = get_object(flow, kwargs[flow.lookup_field])
    # check user has permission to perform transition
    flow.check_user_permissions(user=request.user, new_state=state)
    # check state change is legit
    flow.validate_state_change(obj=obj, new_state=new_state_name)
    # run process hooks
    flow.process(obj=obj, new_state=state, request=request)
    # update object state
    setattr(obj, flow.field, new_state_name)
    obj.save()
    return flow.response(obj=obj)


@require_http_methods(['GET'])
@authenticate
def history(request, flow, **kwargs):
    flow.authenticate(request)
    obj = get_object(flow, kwargs[flow.lookup_field])
    data = obj.yoflow_history.all().values('created_at', 'previous_state', 'new_state', 'user__username', 'meta')  # TODO update user__username
    return JsonResponse(list(data), safe=False)
