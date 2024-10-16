from rest_framework import permissions

class IsAdminorLimitView(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            if request.user.is_staff:
                return True
            else:
                return False
        else:
            return True

class OnlyAdminCanDelete(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return request.user.is_staff
        return True