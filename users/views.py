from django.shortcuts import get_object_or_404
from users.models import User
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import UserSerializer
from .serializers import CustomJWTSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsUserOwner


class UserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class LoginJWTView(TokenObtainPairView):
    serializer_class = CustomJWTSerializer


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsUserOwner]

    def get(self, request: Response, user_id: int) -> Response:
        found_user = get_object_or_404(User, pk=user_id)
        self.check_object_permissions(request, found_user)
        serializer = UserSerializer(found_user)
        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request: Request, user_id: int) -> Response:
        found_user = get_object_or_404(User, pk=user_id)
        self.check_object_permissions(request, found_user)
        serializer = UserSerializer(found_user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = UserSerializer(found_user)

        return Response(serializer.data, status.HTTP_200_OK)
