from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.username


class Movies(models.Model):
    adult = models.BooleanField(blank=True, null=True)
    budget = models.IntegerField(blank=True, null=True)
    homepage = models.CharField(max_length=1000, blank=True, null=True)
    movieid = models.AutoField(primary_key=True)
    imdb_id = models.CharField(max_length=20, blank=True, null=True)
    original_language = models.CharField(max_length=5)
    original_title = models.CharField(max_length=500)
    overview = models.TextField(blank=True, null=True)
    popularity = models.FloatField(blank=True, null=True)
    poster_path = models.CharField(max_length=500, blank=True, null=True)
    release_date = models.DateField()
    revenue = models.IntegerField(blank=True, null=True)
    runtime = models.FloatField()
    status = models.CharField(max_length=20, blank=True, null=True)
    tagline = models.CharField(max_length=1000, blank=True, null=True)
    title = models.CharField(max_length=1000)
    video = models.BooleanField(blank=True, null=True)
    vote_average = models.FloatField(blank=True, null=True)
    vote_count = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'movies'
