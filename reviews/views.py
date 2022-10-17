from django.shortcuts import get_object_or_404
from movies.models import Movie
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView, Request, Response, status
from users.models import User

from reviews.permissions import IsAuthenticatedOrReadOnly

from .serializers import ReviewSerializer


class ReviewView(APIView):
    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        critic = User.objects.get(id=request.user.id)

        review = ReviewSerializer(data=request.data)

        review.is_valid(raise_exception=True)

        review.save(movie=movie, critic=critic)

        return Response(review.data, status.HTTP_201_CREATED)
