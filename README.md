# main

Universium task project.

To run with docker with local configuration (-f production.yml for production)

```sh
docker-compose -f local.yml up
```

To migrate inside docker and create super user, run

```sh
docker-compose -f local.yml run --rm django python manage.py migrate
docker-compose -f local.yml run --rm django python manage.py createsuperuser
```

With same commands, you can run other django commands. For example `importing movie data` from csv files.

```sh
docker-compose -f local.yml run --rm django python manage.py import_movie_data --data-dir=data
```

For running without docker:
- Create virtual env and activate it
- Install requirements
- Run migrations
- Create super user
- Run server

## Performance improvements

You will detect certain `select_related` and `prefetch_related` in the code. This is done to improve performance of the queries. For example, in the `MovieViewSet` class, you will see the following code:

```python
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all().select_related("director").prefetch_related("actors")
    serializer_class = MovieSerializer
```

This is done to avoid N+1 queries. For example, if you don't use `select_related` and `prefetch_related`, you will see the following queries:

Previously, with duplicate queries (N+1)

![duplicate-queries-image](screenshots/Screenshot%202023-01-09%20at%202.55.59%20PM.png)

After using `select_related` and `prefetch_related`
![optimized-queries-image](screenshots/Screenshot%202023-01-09%20at%203.00.37%20PM.png)

### Additional potential improvements

Inside [`import_movie_data`](main/movies/management/commands/import_movie_data.py) script, I am reading objects from csv and inserting per object

There is a possible improvement to read all the objects from csv and then insert them in bulk. This will reduce the number of queries and will improve the performance.

Additionally, you have probably noticed that I am using `get_or_create()`. This is done to avoid duplicate objects. For example, if you have a movie with the same name and director, you will not create a new movie. Instead, you will get the existing movie and update the actors.

Well, there is no `get_or_create` in bulk that comes with django currently, it is probably possible to implement but for this project scope, I don't think it was needed, I just wanted to demonstrate that we can improve things.

If you are sure that you will run import script one time, it could make sense to use bulk create.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

-   To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

-   To create a **superuser account**, use this command:

        $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy main

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).
