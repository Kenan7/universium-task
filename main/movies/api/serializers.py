from main.movies.models import Movie, Genre, Role, Director, DirectorGenre
from rest_framework import serializers


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name',)


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ('first_name', 'last_name')


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('name', 'year', 'rank', 'genres', 'directors')