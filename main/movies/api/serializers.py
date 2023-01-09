from main.movies.models import Movie, Genre, Role, Director, DirectorGenre, Actor
from rest_framework import serializers
from django.db.models import Count


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name',)


class DirectorSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='director.first_name')
    last_name = serializers.CharField(source='director.last_name')

    class Meta:
        model = Director
        fields = ('first_name', 'last_name')


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    directors = DirectorSerializer(many=True)

    class Meta:
        model = Movie
        fields = ('name', 'year', 'rank', 'genres', 'directors')


class TopGenreSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj['name']

    def get_count(self, obj):
        return obj['count']

    class Meta:
        model = Genre
        fields = ('name', 'count')


class PartnerActorSerializer(serializers.ModelSerializer):
    partner_actor_id = serializers.IntegerField(source='id')
    partner_actor_name = serializers.SerializerMethodField()
    number_of_shared_movies = serializers.IntegerField(source='count')

    class Meta:
        model = Actor
        fields = ('partner_actor_id', 'partner_actor_name', 'number_of_shared_movies')

    def get_partner_actor_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'
        

class ActorStatsSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    top_genre = serializers.SerializerMethodField()
    number_of_movies = serializers.SerializerMethodField()
    number_of_movies_by_genre = serializers.SerializerMethodField()
    most_frequent_partner = serializers.SerializerMethodField()

    def get_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    def get_top_genre(self, obj):
        return TopGenreSerializer(
            self.get_number_of_movies_by_genre(obj).first()
        ).data

    def get_number_of_movies(self, obj):
        return obj.roles.count()

    def get_number_of_movies_by_genre(self, obj):
        return (
            Genre.objects.filter(movies__roles__actor=obj)
            .values('name')
            .annotate(count=Count('name'))
            .order_by('-count')
        )
        

    def get_most_frequent_partner(self, obj):
        return PartnerActorSerializer(
            Actor.objects.filter(roles__movie__in=obj.roles.values('movie'))
            .exclude(pk=obj.pk)
            .annotate(count=Count('pk'))
            .order_by('-count')
            .first()
        ).data

    class Meta:
        model = Actor
        fields = [
            'id',
            'name',
            'top_genre',
            'number_of_movies',
            'number_of_movies_by_genre',
            'most_frequent_partner'
        ]