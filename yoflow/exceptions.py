
class FlowException(Exception):

    def __init__(self, message='Server Error', status_code=500, detail=None):
        message = getattr(self, 'message', message) or message
        super(FlowException, self).__init__(message)
        self.status_code = getattr(self, 'status_code', status_code)
        self.detail = detail

    def to_dict(self):
        result = {
            'success': False,
            'message': str(self),
        }
        if self.detail:
            result['detail'] = self.detail
        return result


class InvalidTransition(FlowException):
    status_code = 405


class ObjectNotFound(FlowException):
    status_code = 404
    message = 'Object not found'


class PermissionDenied(FlowException):
    status_code = 403


class ValidationError(FlowException):
    status_code = 400
    message = 'One or more invalid fields'
