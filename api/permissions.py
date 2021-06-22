from rest_framework import permissions
from .models import Roles


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_admin


class IsAdminOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and any([request.user.is_moderator,
                             request.user.is_admin,
                             request.user.id == obj.author.id])))


class IsSafeMethodOrIsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser
