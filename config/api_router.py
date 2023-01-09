from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from main.users.api.views import UserViewSet
from main.movies.api.views import MovieViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("movies", MovieViewSet)


app_name = "api"
urlpatterns = router.urls
