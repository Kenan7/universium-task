import csv
import os

from django.core.management.base import BaseCommand
from django.db import transaction

from main.movies.models import Actor, Director, DirectorGenre, Genre, Movie, MovieDirector, Role


class Command(BaseCommand):
    help = 'Import movie data from csv files'

    def add_arguments(self, parser):
        parser.add_argument('data_dir', type=str)

    def handle(self, *args, **options):
        data_dir = options['data_dir']
        self.stdout.write(self.style.SUCCESS(f'Importing data from {data_dir}'))

        self.import_movies(os.path.join(data_dir, f'{data_dir}_movies.csv'))
        self.import_actors(os.path.join(data_dir, f'{data_dir}_actors.csv'))
        self.import_genres(os.path.join(data_dir, f'{data_dir}_movies_genres.csv'))
        self.import_directors(os.path.join(data_dir, f'{data_dir}_directors.csv'))
        self.import_director_genres(os.path.join(data_dir, f'{data_dir}_directors_genres.csv'))
        self.import_roles(os.path.join(data_dir, f'{data_dir}_roles.csv'))
        self.import_movie_directors(os.path.join(data_dir, f'{data_dir}_movies_directors.csv'))

    @transaction.atomic
    def import_movies(self, file_path):
        self.stdout.write(self.style.SUCCESS(f'Importing movies from {file_path}'))
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Movie.objects.get_or_create(
                    id=row['id'],
                    defaults=dict(
                        name=row['name'],
                        year=row['year'],
                        rank=row['rank'] or 0.0,
                    )
                )
            '''
            Alternate solution is to have all the data in memory with python and
            then use bulk_create to insert all the data in one go. This is faster

            But we are using get_or_create here because we want to avoid duplicates.
            Being sure that we'll only use this script once, we can use bulk_create
            '''
            # 
            # objects = []
            # for row in reader:
            #     movie_obj = Movie(id=row['id'], name=row['name'], year=row['year'], rank=row['rank'] or 0.0)
            #     objects.append(movie_obj)
            # Movie.objects.bulk_create(objects)

    @transaction.atomic
    def import_actors(self, file_path):
        self.stdout.write(self.style.SUCCESS(f'Importing actors from {file_path}'))
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Actor.objects.get_or_create(
                    id=row['id'],
                    defaults=dict(
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                    ),
                )
        
    @transaction.atomic
    def import_genres(self, file_path):
        self.stdout.write(self.style.SUCCESS(f'Importing genres from {file_path}'))
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    movie = Movie.objects.get(id=row['movie_id'])
                    movie.genres.add(Genre.objects.get_or_create(name=row['genre'])[0])
                except Movie.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Movie with id {row["movie_id"]} does not exist'))
                    continue

    @transaction.atomic
    def import_directors(self, file_path):
        self.stdout.write(self.style.SUCCESS(f'Importing directors from {file_path}'))
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Director.objects.get_or_create(
                    id=row['id'],
                    defaults=dict(
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                    ),
                )

    @transaction.atomic
    def import_director_genres(self, file_path):
        self.stdout.write(self.style.SUCCESS(f'Importing director genres from {file_path}'))
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                DirectorGenre.objects.get_or_create(
                    director_id=row['director_id'],
                    genre=row['genre'],
                    defaults=dict(
                        director_id=row['director_id'],
                        genre=row['genre'],
                        prob=row['prob'],
                    ),
                )
    
    
    @transaction.atomic
    def import_roles(self, file_path):
        self.stdout.write(self.style.SUCCESS(f'Importing roles from {file_path}'))
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Role.objects.get_or_create(
                    movie_id=row['movie_id'],
                    actor_id=row['actor_id'],
                    defaults=dict(
                        movie_id=row['movie_id'],
                        actor_id=row['actor_id'],
                        role=row['role'],
                    ),
                )

    @transaction.atomic
    def import_movie_directors(self, file_path):
        self.stdout.write(self.style.SUCCESS(f'Importing movie directors from {file_path}'))
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                MovieDirector.objects.get_or_create(
                    movie_id=row['movie_id'],
                    director_id=row['director_id'],
                    defaults=dict(
                        movie_id=row['movie_id'],
                        director_id=row['director_id'],
                    ),
                )