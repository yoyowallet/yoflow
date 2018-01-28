
def view(request, flow, **kwargs):
    state = request.path.strip('/').split('/')[-1]
    new_state_name = flow.reversed_states[state]
    obj = flow.model.objects.get(**{flow.lookup_field: kwargs[flow.lookup_field]})

    # check user has permission to perform transition
    flow.check_user_permissions(user=request.user, new_state=state)

    # check state change is legit
    flow.validate_state_change(obj=obj, new_state=new_state_name)

    # run process hooks
    response = flow.process(obj=obj, new_state=state, request=request)

    # update object state
    setattr(obj, flow.field, new_state_name)
    obj.save()

    return response
