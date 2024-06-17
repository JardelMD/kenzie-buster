from movies.models import Movie, CategoryRating
from rest_framework import serializers


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    duration = serializers.CharField(default="")
    rating = serializers.ChoiceField(choices=CategoryRating, default=CategoryRating.G)
    synopsis = serializers.CharField(default="")
    added_by = serializers.CharField(read_only=True, source="user.email")

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)
