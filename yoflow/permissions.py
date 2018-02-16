from yoflow.exceptions import PermissionDenied


class Permissions(object):
    
    @staticmethod
    def authenticate(request):
        if not request.user.is_authenticated:
            raise PermissionDenied('User not authenticated')

    @staticmethod
    def can_create(request):
        raise PermissionDenied('You do not have permission to create new instances')

    @staticmethod
    def can_delete(request):
        raise PermissionDenied('You do not have permission to delete instances')

    @staticmethod
    def can_view_history(request):
        raise PermissionDenied('You do not have permission to view instance history')