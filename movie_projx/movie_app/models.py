from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    birth_date = models.DateField(null=True)

    def __str__(self):
        return self.user.username


class Casts(models.Model):
    id = models.AutoField(primary_key=True)
    character = models.CharField(max_length=200)
    credit_id = models.CharField(max_length=250, blank=True, null=True)
    gender = models.IntegerField()
    movie = models.ForeignKey('Movies', models.DO_NOTHING)
    name = models.CharField(max_length=200)
    order = models.IntegerField()
    profile_path = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'casts'


class Genres(models.Model):
    genreid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'genres'


class Languages(models.Model):
    iso_639_1 = models.CharField(primary_key=True, max_length=2)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'languages'


class MovieRatings(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userid', blank=True, null=True)
    movieid = models.ForeignKey('Movies', models.DO_NOTHING, db_column='movieid', blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    rating = models.FloatField()
    title = models.CharField(max_length=70, blank=False, null=True)
    description = models.CharField(max_length=500, blank=False, null=True)
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)

    def __str__(self):
        return self.rating

    class Meta:
        db_table = 'movie_ratings'

class MovieRatingsVotes(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey(User, models.DO_NOTHING, db_column='userid', blank=False, null=False)
    movie_rating_id = models.ForeignKey('MovieRatings', models.DO_NOTHING, db_column='movieratingid', blank=False, null=False)
    vote = models.BooleanField(null=False)

    class Meta:
        db_table = 'movie_ratings_votes'


class Movies(models.Model):
    adult = models.BooleanField(blank=True, null=True)
    budget = models.IntegerField(blank=True, null=True)
    homepage = models.CharField(max_length=1000, blank=True, null=True)
    movieid = models.AutoField(primary_key=True)
    imdb_id = models.CharField(max_length=20, blank=True, null=True)
    original_language = models.CharField(max_length=2, blank=True, null=True)
    original_title = models.CharField(max_length=500)
    overview = models.TextField(blank=True, null=True)
    popularity = models.FloatField(blank=True, null=True)
    poster_path = models.CharField(max_length=500, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    revenue = models.IntegerField(blank=True, null=True)
    runtime = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    tagline = models.CharField(max_length=1000, blank=True, null=True)
    title = models.CharField(max_length=1000)
    video = models.BooleanField(blank=True, null=True)
    vote_average = models.FloatField(blank=True, null=True)
    vote_count = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'movies'


class MoviesGenres(models.Model):
    id = models.AutoField(primary_key=True)
    genre = models.ForeignKey(Genres, models.DO_NOTHING)
    movie = models.ForeignKey(Movies, models.DO_NOTHING)

    class Meta:
        db_table = 'movies_genres'


class MoviesLanguages(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movies, models.DO_NOTHING)
    language = models.ForeignKey(Languages, models.DO_NOTHING)

    class Meta:
        db_table = 'movies_languages'


class MoviesProductioncompanies(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movies, models.DO_NOTHING)
    productioncompanies = models.ForeignKey('Productioncompanies', models.DO_NOTHING)

    class Meta:
        db_table = 'movies_productioncompanies'


class MoviesProductioncountries(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movies, models.DO_NOTHING)
    productioncountry_iso = models.ForeignKey('Productioncountries', models.DO_NOTHING, db_column='productioncountry_iso')

    class Meta:
        db_table = 'movies_productioncountries'


class Productioncompanies(models.Model):
    productioncompanyid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'productioncompanies'


class Productioncountries(models.Model):
    iso_639_1 = models.CharField(primary_key=True, max_length=2)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'productioncountries'
