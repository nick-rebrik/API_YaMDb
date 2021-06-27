from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_admin


class IsAdminOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and any([request.user.is_moderator,
                             request.user.is_admin,
                             request.user.id == view.get_object().author.id]
                            )
                    )
                )


class IsSafeMethodOrIsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser)
