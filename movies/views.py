from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView, Request, Response, status

from movies.serializers import MovieSerializer

from .permissions import IsAdminOrReadOnly


class MovieViews(APIView):
    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAdminOrReadOnly]

    def post(self, request: Request) -> Response:
        movie = MovieSerializer(data=request.data)

        movie.is_valid(raise_exception=True)

        movie.save()

        return Response(movie.data, status.HTTP_201_CREATED)
