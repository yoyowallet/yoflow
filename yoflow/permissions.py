
class Permissions(object):

    @staticmethod
    def authenticate(request):
        return request.user.is_authenticated

    @staticmethod
    def can_create(request):
        return False

    @staticmethod
    def can_delete(request):
        return False

    @staticmethod
    def can_view_history(request):
        return False
