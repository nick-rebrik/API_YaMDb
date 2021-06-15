from rest_framework import permissions
from .models import MyUser

class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)

class IsAdminOrReadOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return  (request.user.is_authenticated)
    
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS or 
            (request.user.is_authenticated and 
            request.user.role in [MyUser.Roles.ADMIN, MyUser.Roles.MODERATOR]
            ))
    