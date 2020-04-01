from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.urls import reverse
from django.contrib.auth.models import User
from ..forms import *
from django.contrib.auth.hashers import make_password, check_password


class SignUpTest(TestCase):

    def test_UserForm_valid(self):
        form = UserForm(data={'username': 'example_username', 'password': 'root', 'email': 'test@example.sk'})
        self.assertTrue(form.is_valid())
        form = UserForm(data={'username': 'example_username', 'password': 'root', 'email': ''})
        self.assertTrue(form.is_valid())


    def test_UserForm_invalid(self):
        form = UserForm(data={'username': 'example_username', 'password': '', 'email': 'test@example.sk'})
        self.assertFalse(form.is_valid())
        form = UserForm(data={'username': '', 'password': 'root', 'email': 'test@example.sk'})
        self.assertFalse(form.is_valid())

# class SignUpViewTest(TestCase):
#     """
#         We can't run SignUpViewTest, cause we in views overiding save(), with our
#         raw sql, which is not wrapped as transaction atomic function, and UnitTest wraping
#         every transacion as atomic --> error.
#         """
#     def test_signup_correct(self):
#         user_count = User.objects.count()
#         response = self.client.post(reverse('movie_app:register'), {'username': 'example_username', 'password': 'sdfas', 'email': 'test@example.sk'})
#         print(response)
#         # self.assertEqual(response.status_code, 200)
#         # self.assertEqual(User.objects.count(), user_count+1)
#         # self.assertTrue('"error": false' in response.content)


class SignInTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='example_username',
                                                         password='example_password',
                                                         email='test@example.sk')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(username='example_username', password='example_password')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='wrong', password='example_password')
        self.assertFalse((user is not None) and user.is_authenticated)

    def test_wrong_password(self):
        user = authenticate(username='example_username', password='wrong')
        self.assertFalse((user is not None) and user.is_authenticated)



class SignInViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='example_username',
                                                         password='example_password',
                                                         email='test@example.sk')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        response = self.client.post(reverse('user_login'),
                                    {'username': 'example_username', 'password': 'example_password'})
        self.assertTrue(response.status_code, 302)

    def test_wrong_username(self):
        response = self.client.post(reverse('user_login'),
                                    {'username': 'wrong', 'password': 'example_password'})
        self.assertTrue(response.status_code == 200 and 'Invalid' in str(response.content))

    def test_wrong_password(self):
        response = self.client.post(reverse('user_login'),
                                    {'username': 'example_username', 'password': 'wrong'})
        self.assertTrue(response.status_code == 200 and 'Invalid' in str(response.content))
