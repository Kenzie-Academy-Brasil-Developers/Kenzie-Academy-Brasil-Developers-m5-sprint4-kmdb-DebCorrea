from django.shortcuts import get_object_or_404
from movies.models import Movie
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView, Request, Response, status
from users.models import User

from reviews.permissions import IsAdminOrOwner, IsAuthenticatedOrReadOnly

from .models import Review
from .serializers import ReviewSerializer


class ReviewView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        critic = User.objects.get(id=request.user.id)

        review = ReviewSerializer(data=request.data)

        review.is_valid(raise_exception=True)

        review.save(movie=movie, critic=critic)

        return Response(review.data, status.HTTP_201_CREATED)

    def get(self, request: Request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)

        reviews = Review.objects.filter(movie=movie)

        result_page = self.paginate_queryset(reviews, request, view=self)

        reviews_obj = ReviewSerializer(result_page, many=True)

        return self.get_paginated_response(reviews_obj.data)


class ReviewDetailView(APIView):
    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrOwner]

    def get(self, request: Request, movie_id: int, review_id: int) -> Response:
        review = get_object_or_404(Review, id=review_id)

        review_obj = ReviewSerializer(review)

        return Response(review_obj.data)

    def delete(
        self,
        request: Request,
        movie_id: int,
        review_id: int,
    ) -> Response:
        review = get_object_or_404(Review, id=review_id)

        self.check_object_permissions(request, review)

        review.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
