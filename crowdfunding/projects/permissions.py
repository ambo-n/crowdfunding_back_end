from rest_framework import permissions
from users .models import CustomUser

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner ==request.user

class IsAdminorLimitView(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            if request.user.is_staff:
                return True
            else:
                return False
        else:
            return True
        
class IsSupporterOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            if request.user == obj.support or request.user.is_staff:
                return True
        return obj.support == request.user