from rest_framework import permissions
from rest_framework.views import Request, View

from users.models import User


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return request.user.is_authenticated and request.user.is_superuser


class IsAdminOrOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: User):
        return (
            request.user.is_authenticated
            and request.user.is_superuser
            or request.user.id == obj.id
        )
