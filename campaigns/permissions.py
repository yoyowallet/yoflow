from yoflow import permissions


class Permissions(permissions.Permissions):

    @staticmethod
    def authenticate(request):
        return True

    @staticmethod
    def can_create(request):
        return True

    @staticmethod
    def has_draft_permission(request):
        return True

    @staticmethod
    def has_pending_permission(request):
        return True

    @staticmethod
    def has_rejected_permission(request):
        return True

    @staticmethod
    def has_approved_permission(request):
        return True

    @staticmethod
    def has_deleted_permission(request):
        return True