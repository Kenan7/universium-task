from django_filters.filterset import FilterSet
from django_filters import CharFilter
from main.movies.models import Movie


class MovieFilter(FilterSet):
    genre = CharFilter(field_name='genre__name', lookup_expr='iexact', label='Genre name')
    first_name = CharFilter(field_name='directors__director__first_name', lookup_expr='iexact', label='Director first name')
    last_name = CharFilter(field_name='directors__director__last_name', lookup_expr='iexact', label='Director last name')

    class Meta:
        model = Movie
        fields = ['genre', 'first_name', 'last_name']
