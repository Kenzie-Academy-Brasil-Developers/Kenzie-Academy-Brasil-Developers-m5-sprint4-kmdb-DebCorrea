import ipdb
from genres.models import Genre
from genres.serializers import GenreSerializer
from rest_framework import serializers

from movies.models import Movie


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    duration = serializers.CharField(max_length=10)
    premiere = serializers.DateField()
    classification = serializers.IntegerField()
    synopsis = serializers.CharField()
    genres = GenreSerializer(many=True)

    def create(self, validated_data: dict) -> Movie:
        genres = validated_data.pop("genres")

        movie = Movie.objects.create(**validated_data)

        for genre in genres:
            genre_obj, _ = Genre.objects.get_or_create(**genre)

            movie.genres.add(genre_obj)

        return movie

    def update(self, instance: Movie, validated_data: dict) -> Movie:
        for key, value in validated_data.items():
            if key == "genres":

                genres = []

                for genre in value:
                    genre_obj, _ = Genre.objects.get_or_create(**genre)

                    genres.append(genre_obj)

                instance.genres.set(genres)
            else:
                setattr(instance, key, value)

        instance.save()

        return instance
