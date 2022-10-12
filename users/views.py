from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView, Request, Response, status

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
