from rest_framework import permissions
from rest_framework.views import Request, View

from reviews.models import Review


class IsAuthenticatedOrReadOnly(permissions.BasePermission):

    SAFE_METHODS = ("GET", "HEAD", "OPTIONS")

    def has_permission(self, request: Request, view: View):
        return (
            request.method in self.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_superuser or request.user.is_critic)
        )


class IsAdminOrOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Review):
        return (
            request.user.is_authenticated
            and request.user.is_superuser
            or request.user.id == obj.critic.id
        )
