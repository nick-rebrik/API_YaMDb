from rest_framework import permissions
from .models import MyUser


class IsAdmin(permissions.BasePermission):
   
    def has_permission(self, request, view):
        return (request.user.role == MyUser.Roles.ADMIN or 
            request.user.is_superuser==True)

    def has_object_permission(self, request, view, obj):
        return (request.user.role == MyUser.Roles.ADMIN or 
            request.user.is_superuser==True or
            request.user.id==obj.id)
    
class IsAdminOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS or
            (request.user.is_authenticated and 
            any ([request.user.role in [MyUser.Roles.ADMIN, MyUser.Roles.MODERATOR],
            request.user.is_superuser==True,
            request.user.id==obj.author.id])))

class IsSafeMethodOrIsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS or
            request.user.role == MyUser.Roles.ADMIN or 
            request.user.is_superuser==True)

    def has_object_permission(self, request, view, obj):    
        return (request.user.role == MyUser.Roles.ADMIN or 
            request.user.is_superuser==True)

