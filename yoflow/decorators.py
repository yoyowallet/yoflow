from functools import wraps


def transition(to_state):
    def decorator(view):
        @wraps(view)
        def wrapper(self, *args, **kwargs):
            flow = self.flow()
            # process custom validation logic
            meta = flow.validate(self)
            # fetch instance
            obj = self.get_object()
            # validate state change
            flow.check_permissions(obj=obj, to_state=to_state)
            # process view logic
            result = view(self, *args, **kwargs)
            # process flow logic
            flow.process(obj=obj, to_state=to_state, meta=meta, request=self.request)
            return result
        return wrapper
    return decorator
