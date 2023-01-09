from django.test import TestCase
from main.movies.management.commands.import_movie_data import Command
from main.movies.models import Actor, Director, DirectorGenre, Genre, Movie, MovieDirector, Role

class ImportMovieDataTestCase(TestCase):
    def test_import_movies(self):
        command = Command()

        command.import_movies('main/movies/tests/test_data_movies.csv')

        self.assertEqual(3, Movie.objects.count())

    def test_import_actors(self):
        command = Command()

        command.import_actors('main/movies/tests/test_data_actors.csv')

        self.assertEqual(3, Actor.objects.count())

    def test_import_genres_and_relations(self):
        command = Command()

        command.import_movies('main/movies/tests/test_data_movies.csv')
        command.import_genres('main/movies/tests/test_data_movies_genres.csv')

        self.assertEqual(3, Genre.objects.count())
        self.assertEqual(1, Movie.objects.get(id=1).genres.count())

    def test_import_directors(self):
        command = Command()

        command.import_movies('main/movies/tests/test_data_movies.csv')
        command.import_directors('main/movies/tests/test_data_directors.csv')

        self.assertEqual(3, Director.objects.count())

    def test_import_director_genres(self):
        command = Command()

        command.import_directors('main/movies/tests/test_data_directors.csv')
        command.import_director_genres('main/movies/tests/test_data_directors_genres.csv')

        self.assertEqual(3, DirectorGenre.objects.count())

    def test_import_roles_and_relations(self):
        command = Command()

        command.import_movies('main/movies/tests/test_data_movies.csv')
        command.import_actors('main/movies/tests/test_data_actors.csv')
        command.import_roles('main/movies/tests/test_data_roles.csv')

        self.assertEqual(3, Role.objects.count())
        self.assertEqual(2, Movie.objects.get(id=0).roles.count())
        self.assertEqual(2, Actor.objects.get(id=2).roles.count())

    def test_import_movie_directors(self):
        command = Command()

        command.import_movies('main/movies/tests/test_data_movies.csv')
        command.import_directors('main/movies/tests/test_data_directors.csv')
        command.import_movie_directors('main/movies/tests/test_data_movies_directors.csv')

        self.assertEqual(3, MovieDirector.objects.count())