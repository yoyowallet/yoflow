
class Permissions(object):

    @staticmethod
    def authenticate(request):
        return request.user.is_authenticated

    @staticmethod
    def can_create(request):
        return False

    @staticmethod
    def can_delete(request, obj):
        return False

    @staticmethod
    def can_view_history(request, obj):
        return False
