from rest_framework import permissions
from rest_framework.views import Request, View


class IsAuthenticatedOrReadOnly(permissions.BasePermission):

    SAFE_METHODS = ("GET", "HEAD", "OPTIONS")

    def has_permission(self, request: Request, view: View):
        return (
            request.method in self.SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_superuser or request.user.is_critic)
        )
