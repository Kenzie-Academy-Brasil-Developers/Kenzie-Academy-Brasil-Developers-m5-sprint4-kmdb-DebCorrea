from movies.models import Movie
from rest_framework import serializers
from users.models import User

from reviews.exceptions import DuplicatedReviewError
from reviews.models import Review


class CriticSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ["id", "first_name", "last_name"]


class ReviewSerializer(serializers.ModelSerializer):
    critic = CriticSerializer(read_only=True)

    class Meta:
        model = Review

        fields = [
            "id",
            "stars",
            "review",
            "spoilers",
            "recomendation",
            "movie",
            "critic",
        ]

        read_only_fields = ["movie"]

    def create(self, validated_data: dict) -> Review:
        if self.duplicated_review(validated_data["movie"], validated_data["critic"]):
            raise DuplicatedReviewError()

        review = Review.objects.create(**validated_data)

        return review

    def duplicated_review(self, movie: Movie, critic: User) -> bool:
        critic_review = Review.objects.filter(critic=critic)

        if critic_review:
            movie_critic_review = critic_review.filter(movie=movie)

            if movie_critic_review:
                return True

        return False
