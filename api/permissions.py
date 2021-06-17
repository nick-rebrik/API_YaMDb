from rest_framework import permissions
from .models import MyUser


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


class IsAdmin(permissions.BasePermission):
   
    def has_permission(self, request, view):
        return (request.user.role == MyUser.Roles.USER)

    def has_object_permission(self, request, view, obj):
        return request.user.role == MyUser.Roles.ADMIN

