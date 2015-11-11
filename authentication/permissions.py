from rest_framework import permissions


class IsUserOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, user):
        if request.user:
            return user == request.user
        return False


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user:
            return request.user.is_superuser
        return False
