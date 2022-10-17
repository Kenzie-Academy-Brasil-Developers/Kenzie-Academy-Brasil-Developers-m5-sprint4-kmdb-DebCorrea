from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView, Request, Response, status

from movies.serializers import MovieSerializer

from .models import Movie
from .permissions import IsAdminOrReadOnly


class MovieView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAdminOrReadOnly]

    def post(self, request: Request) -> Response:
        movie = MovieSerializer(data=request.data)

        movie.is_valid(raise_exception=True)

        movie.save()

        return Response(movie.data, status.HTTP_201_CREATED)

    def get(self, request: Request):
        movies = Movie.objects.all()

        result_page = self.paginate_queryset(movies, request, view=self)

        movies_serializer = MovieSerializer(result_page, many=True)

        return self.get_paginated_response(movies_serializer.data)


class MovieDetailView(APIView):
    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAdminOrReadOnly]

    def get(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        movie_obj = MovieSerializer(movie)

        return Response(movie_obj.data)

    def patch(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        movie_obj = MovieSerializer(movie, request.data, partial=True)

        movie_obj.is_valid(raise_exception=True)

        movie_obj.save()

        return Response(movie_obj.data)

    def delete(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        movie.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
