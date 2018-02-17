from yoflow.exceptions import PermissionDenied


class Permissions(object):
    
    @staticmethod
    def authenticate(request):
        return request.user.is_authenticated

    @staticmethod
    def can_create(request):
        return false

    @staticmethod
    def can_delete(request):
        return false

    @staticmethod
    def can_view_history(request):
        return false