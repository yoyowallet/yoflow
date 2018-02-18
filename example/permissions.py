from yoflow import permissions


class ParentPermissions(permissions.Permissions):

    @staticmethod
    def authenticate(request):
        return True

    @staticmethod
    def can_create(request):
        return True

    @staticmethod
    def can_delete(request, obj):
        return True

    @staticmethod
    def can_view_history(request, obj):
        return True

    @staticmethod
    def has_draft_permission(request, obj):
        return True

    @staticmethod
    def has_approved_permission(request, obj):
        return True

    @staticmethod
    def has_final_permission(request, obj):
        return True
