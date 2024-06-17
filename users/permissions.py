from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView
from .models import User


class IsAdminOrReadOlnly(BasePermission):
    def has_permission(self, request: Request, view: APIView):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_superuser
        )


class IsUserOwner(BasePermission):
    def has_object_permission(self, request: Request, view: APIView, obj: User):
        return request.user.is_authenticated and (
            obj == request.user or request.user.is_superuser
        )
