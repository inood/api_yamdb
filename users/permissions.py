from rest_framework import permissions
from .models import Roles


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated and
                obj.author == request.user)


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role == Roles.MODERATOR)

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and request.user.role == Roles.MODERATOR)


class IsAdminOrStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.role == Roles.ADMIN
                     or request.user.is_staff))

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and (request.user.role == Roles.ADMIN
                     or request.user.is_staff))
