from django.urls import path

from main.movies.api.views import ActorStatsView


urlpatterns = [
    path('actor_stats/<int:pk>/', ActorStatsView.as_view(), name='actor_stats'),
]