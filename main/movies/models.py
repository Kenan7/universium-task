from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100)
    movies = models.ManyToManyField('Movie', related_name='genres')

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    rank = models.FloatField()


class Actor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)


class Role(models.Model):
    movie = models.ForeignKey(Movie, related_name='roles', on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, related_name='roles', on_delete=models.CASCADE)
    role = models.CharField(max_length=100)


class Director(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class MovieDirector(models.Model):
    movie = models.ForeignKey(Movie, related_name='directors', on_delete=models.CASCADE)
    director = models.ForeignKey(Director, related_name='movies', on_delete=models.CASCADE)


class DirectorGenre(models.Model):
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    genre = models.CharField(max_length=100)
    prob = models.FloatField()
