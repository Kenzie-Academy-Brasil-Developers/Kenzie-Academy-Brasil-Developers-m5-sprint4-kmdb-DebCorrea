from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView, Request, Response, status

from .models import User
from .permissions import IsAdmin, IsAdminOrOwner
from .serializers import UserLoginSerializer, UserSerializer


class UserRegisterView(APIView):
    def post(self, request: Request) -> Response:
        user = UserSerializer(data=request.data)

        user.is_valid(raise_exception=True)

        user.save()

        return Response(user.data, status.HTTP_201_CREATED)


class UserLoginView(APIView):
    def post(self, request: Request) -> Response:
        login_serializer = UserLoginSerializer(data=request.data)

        login_serializer.is_valid(raise_exception=True)

        user = authenticate(**login_serializer.validated_data)

        if not user:
            return Response(
                {"detail": "invalid username or password"},
                status.HTTP_400_BAD_REQUEST,
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key})


class UserView(APIView):
    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAdmin]

    def get(self, request: Request) -> Response:
        users = User.objects.all()

        users_serializer = UserSerializer(users, many=True)

        return Response(users_serializer.data)


class UserDetailView(APIView):
    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAdminOrOwner]

    def get(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(User, id=user_id)

        self.check_object_permissions(request, user)

        user_serializer = UserSerializer(user)

        return Response(user_serializer.data)
