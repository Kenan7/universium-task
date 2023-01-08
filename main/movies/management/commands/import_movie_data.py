import csv
import os

from django.core.management.base import BaseCommand
from django.db import transaction

from movies.models import Actor, Director, DirectorGenre, Genre, Movie, MovieDirector, Role


class Command(BaseCommand):
    help = 'Import movie data from csv files'

    def add_arguments(self, parser):
        parser.add_argument('data_dir', type=str)

    def handle(self, *args, **options):
        data_dir = options['data_dir']
        self.stdout.write(self.style.SUCCESS(f'Importing data from {data_dir}'))

        self.import_movies(os.path.join(data_dir, 'movies.csv'))
        self.import_genres(os.path.join(data_dir, 'genres.csv'))
        self.import_directors(os.path.join(data_dir, 'directors.csv'))
        self.import_director_genres(os.path.join(data_dir, 'director_genres.csv'))
        self.import_actors(os.path.join(data_dir, 'actors.csv'))
        self.import_roles(os.path.join(data_dir, 'roles.csv'))
        self.import_movie_directors(os.path.join(data_dir, 'movie_directors.csv'))

    @transaction.atomic
    def import_movies(self, file_path):
        self.stdout.write(self.style.SUCCESS(f'Importing movies from {file_path}'))
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Movie.objects.create(
                    name=row['name'],
                    year=row['year'],
                    rank=row['rank'],
                )
        
    @transaction.atomic
    def import_genres(self, file_path):
        self.stdout.write(self.style.SUCCESS(f'Importing genres from {file_path}'))
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Genre.objects.create(
                    name=row['name'],
                    movie_id=row['movie_id'],
                )

    @transaction.atomic
    def import_directors(self, file_path):
        self.stdout.write(self.style.SUCCESS(f'Importing directors from {file_path}'))
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Director.objects.create(
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                )

    @transaction.atomic
    def import_director_genres(self, file_path):
        self.stdout.write(self.style.SUCCESS(f'Importing director genres from {file_path}'))
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                DirectorGenre.objects.create(
                    director_id=row['director_id'],
                    genre=row['genre'],
                    prob=row['prob'],
                )
    
    @transaction.atomic
    def import_actors(self, file_path):
        self.stdout.write(self.style.SUCCESS(f'Importing actors from {file_path}'))
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Actor.objects.create(
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                )
    
    @transaction.atomic
    def import_roles(self, file_path):
        self.stdout.write(self.style.SUCCESS(f'Importing roles from {file_path}'))
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Role.objects.create(
                    movie_id=row['movie_id'],
                    actor_id=row['actor_id'],
                    role=row['role'],
                )

    @transaction.atomic
    def import_movie_directors(self, file_path):
        self.stdout.write(self.style.SUCCESS(f'Importing movie directors from {file_path}'))
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                MovieDirector.objects.create(
                    movie_id=row['movie_id'],
                    director_id=row['director_id'],
                )
    