from yoflow import permissions


class ParentPermissions(permissions.Permissions):

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
    def has_approved_permission(request):
        pass

    @staticmethod
    def has_final_permission(request):
        pass
