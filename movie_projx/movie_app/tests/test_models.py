from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.urls import reverse
from django.contrib.auth.models import User
from ..forms import *
from django.contrib.auth.hashers import make_password, check_password
from movie_app.models import UserProfileInfo
from datetime import datetime


class AddMovieTest(TestCase):
    def setUp(self):
        self.count = Movies.objects.count()
        self.movie = Movies(original_language='SK', original_title='hello world', release_date=datetime.now(), runtime=120.0, title="this is title")
        self.movie.save()

    def tearDown(self):
        self.movie.delete()

    def test_correct(self):
        self.assertEqual(Movies.objects.count(), self.count+1)

class SearchMovieViewTest(TestCase):
    def setUp(self):
        self.movie = Movies(original_language='SK', original_title='hello world', release_date=datetime.now(),
                            runtime=120.0, title="this is title")
        self.movie.save()

    def tearDown(self):
        self.movie.delete()

    def isInResults(self, movie, results):
        for m in results:
            if m.movieid == movie.movieid:
                return True
        return False

    def test_correct(self):
        response = self.client.post(str(reverse('movie_app:search_results') + '?q=thi'))
        self.assertTrue((response.status_code == 200) and self.isInResults(self.movie, response.context['movies']))

class getMovieDetailsViewTest(TestCase):
    def setUp(self):
        self.movie = Movies(original_language='SK', original_title='hello world', release_date=datetime.now(),
                            runtime=120.0, title="this is title")
        self.movie.save()

    def tearDown(self):
        self.movie.delete()

    def test_correct(self):
        response = self.client.post(reverse('movie_app:details', kwargs={'movie_id':self.movie.movieid}))
        response_movie = response.context['movie']
        self.assertTrue((response.status_code == 200) and response_movie and response_movie.movieid == self.movie.movieid)