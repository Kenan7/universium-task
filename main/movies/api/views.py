from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import NotFound


from main.movies.models import Movie, Actor
from main.movies.api.serializers import MovieSerializer, ActorStatsSerializer
from main.movies.api.filters import MovieFilter


class MoviePagination(PageNumberPagination):
    page_size = 100


class MovieViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    model = Movie
    queryset = Movie.objects.all().prefetch_related('genres', 'directors__director')
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MovieFilter
    pagination_class = MoviePagination


class ActorStatsView(RetrieveModelMixin, APIView):
    model = Actor
    queryset = Actor.objects.all().prefetch_related('movies')
    serializer_class = ActorStatsSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        instance = self.get_object(kwargs['pk'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_object(self, pk):
        try:
            return Actor.objects.get(pk=pk)
        except Actor.DoesNotExist:
            raise NotFound

    def get_serializer(self, instance):
        return ActorStatsSerializer(instance)