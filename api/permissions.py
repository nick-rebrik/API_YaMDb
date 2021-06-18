from rest_framework import permissions
from .models import MyUser


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


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
            request.user.role in [MyUser.Roles.ADMIN, MyUser.Roles.MODERATOR] or
            request.user.is_superuser==True or 
            request.user.id==obj.user.id)
