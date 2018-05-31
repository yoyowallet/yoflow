from functools import wraps


def transition(to_state):
    def decorator(view):
        @wraps(view)
        def wrapper(self, *args, **kwargs):
            flow = self.flow()
            meta = flow.validate(self)
            result = view(self, *args, **kwargs)
            flow.process(obj=self.get_object(), to_state=to_state, meta=meta, request=self.request)
            return result
        return wrapper
    return decorator
