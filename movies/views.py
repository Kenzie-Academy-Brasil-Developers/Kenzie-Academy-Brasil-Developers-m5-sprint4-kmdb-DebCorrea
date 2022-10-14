from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView, Request, Response, status

from movies.serializers import MovieSerializer

from .models import Movie
from .permissions import IsAdminOrReadOnly


class MovieView(APIView):
    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAdminOrReadOnly]

    def post(self, request: Request) -> Response:
        movie = MovieSerializer(data=request.data)

        movie.is_valid(raise_exception=True)

        movie.save()

        return Response(movie.data, status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        movies = Movie.objects.all()

        movies_serializer = MovieSerializer(movies, many=True)

        return Response(movies_serializer.data)


class MovieDetailView(APIView):
    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        movie_obj = MovieSerializer(movie)

        return Response(movie_obj.data)

    def delete(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        movie.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
