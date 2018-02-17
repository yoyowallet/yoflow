
class FlowException(Exception):

    def __init__(self, message='Server Error', status_code=500):
        super(FlowException, self).__init__(message)
        self.status_code = getattr(self, 'status_code', status_code)

    def to_dict(self):
        return {
            'success': False,
            'message': str(self),
        }


class InvalidTransition(FlowException):
    status_code = 405


class ObjectNotFound(FlowException):
    status_code = 404


class PermissionDenied(FlowException):
    status_code = 403
