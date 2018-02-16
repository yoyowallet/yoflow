from yoflow import permissions


class Permissions(permissions.Permissions):

    @staticmethod
    def authenticate(request):
        pass

    @staticmethod
    def can_create(request):
        pass

    @staticmethod
    def has_draft_permission(request):
        pass

    @staticmethod
    def has_pending_permission(request):
        pass

    @staticmethod
    def has_rejected_permission(request):
        pass

    @staticmethod
    def has_approved_permission(request):
        pass

    @staticmethod
    def has_deleted_permission(request):
        pass