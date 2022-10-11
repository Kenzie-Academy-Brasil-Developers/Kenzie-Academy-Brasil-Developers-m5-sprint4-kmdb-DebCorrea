from rest_framework.views import APIView, Request, Response, status

from .serializers import UserSerializer


class UserRegisterView(APIView):
    def post(self, request: Request) -> Response:
        user = UserSerializer(data=request.data)

        user.is_valid(raise_exception=True)

        user.save()

        return Response(user.data, status.HTTP_201_CREATED)
