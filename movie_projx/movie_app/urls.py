from django.conf.urls import url
from django.urls import path
from . import views

# SET THE NAMESPACE!
app_name = 'movie_app'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns = [
    url('^$', views.list_movies, name='list_movies'),
    path('details/<int:movie_id>/', views.movie_details, name='details'),
    path('search/',  views.search_results, name='search_results'),
]
