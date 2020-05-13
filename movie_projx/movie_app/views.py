import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import *
from django.core.paginator import Paginator
from django.db import connection
from django.db.models import Q
from django.db.models.functions import ExtractYear
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from movie_projx import settings
from .forms import UserForm, UserProfileInfoForm, MovieRatingsForm
from .models import Movies, Genres, Languages, MoviesGenres, Productioncountries, Productioncompanies, Casts, \
    MovieRatings, MovieRatingsVotes
from django.db.models import *

from django.forms.models import model_to_dict

from django.contrib.auth.models import User


def get_row(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        row = cursor.fetchone()
        cursor.close()
        return row


def get_all_rows(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        row = cursor.fetchall()
        cursor.close()
        return row


def gen_add_user_sql(_username, _email, _password):
    passw = make_password(_password, salt=None, hasher='default')
    add_user_script = f"""INSERT INTO auth_user(password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
        SELECT '{passw}', NOW(), FALSE, '{_username}', '', '', '{_email}', FALSE, TRUE, NOW()
        WHERE NOT EXISTS(
                SELECT username FROM auth_user WHERE username='{_username}'
                );"""
    return add_user_script


def index(request):
    return render(request, 'movie_app/index.html')


@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def handle_uploaded_file(f, file_path):
    print("file_path: ", file_path)
    with open('..' + file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            print(user_form.cleaned_data['username'])
            print(user_form.cleaned_data['password'])
            print(user_form.cleaned_data['email'])
            with connection.cursor() as cur:
                cur.execute(
                    gen_add_user_sql(user_form.cleaned_data['username'], user_form.cleaned_data['email'],
                                     user_form.cleaned_data['password']))
                connection.commit()
                cur.execute(f"""SELECT id FROM auth_user WHERE username='{user_form.cleaned_data['username']}'""")
                user_id = cur.fetchone()[0]
                print("user_id: ", user_id)
                profile_pic_path = ""
                if 'profile_pic' in request.FILES:
                    print('found it')
                    profile_pic_path = request.FILES['profile_pic']
                    timestamp_str = datetime.now().strftime("%d_%b_%Y_%H_%M_%S_%f)")
                    dest_path = '/movie_projx' + settings.MEDIA_URL + 'profile_pics/' + str(
                        f'{timestamp_str}_' + str(profile_pic_path))
                    handle_uploaded_file(request.FILES['profile_pic'], dest_path)
                    cur.execute(f"""
                                        INSERT INTO movie(profile_pic, user_id) SELECT '{profile_pic_path}', {user_id};
                                    """)
                connection.commit()
                cur.close()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'movie_app/registration.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        row = get_row(f"""SELECT password, is_active FROM auth_user WHERE username='{username}'""")
        if row is None:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details given")
        password_encoded = row[0]
        user_is_active = row[1]
        if password is not None:
            if check_password(password, password_encoded):
                if user_is_active:
                    print("is active")
                    login(request, authenticate(username=username, password=password))
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return HttpResponse("Your account was inactive.")
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username, password))
                return HttpResponse("Invalid login details given")
    else:
        return render(request, 'movie_app/login.html', {})


def list_movies(request):
    genres = Genres.objects.all()
    languages = Languages.objects.all()
    movie_list = Movies.objects.all()
    paginator = Paginator(movie_list, 25)  # Show 25 movies per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    sort_types = [{"name": "Popularity (most to least)", "id": "pop_desc"},
                  {"name": "Popularity (least to most)", "id": "pop_asc"},
                  {"name": "Release date (newest to oldest)", "id": "rel_new"},
                  {"name": "Release date (oldest to newest)", "id": "rel_old"},
                  {"name": "Reviews (most to least)", "id": "row_desc"},
                  {"name": "Reviews (least to most)", "id": "row_asc"}]

    return render(request, 'movie_app/movies.html',
                  {'page_obj': page_obj, 'genres': genres, 'languages': languages, 'sort_types': sort_types})


def movie_details(request, movie_id):
    movie_obj = Movies.objects.raw(f"""SELECT * FROM movies WHERE movieid = {movie_id} LIMIT 1""")[0]
    genres = Genres.objects.raw(
        f"""SELECT * FROM genres INNER JOIN movies_genres ON (genres.genreid = movies_genres.genre_id) WHERE movies_genres.movie_id = {movie_id}""")
    production_countries = Productioncountries.objects.raw(
        f"""SELECT * FROM productioncountries INNER JOIN movies_productioncountries ON (productioncountries.iso_639_1 = movies_productioncountries.productioncountry_iso) WHERE movies_productioncountries.movie_id = {movie_id}""")
    production_companies = Productioncompanies.objects.raw(
        f"""SELECT * FROM productioncompanies INNER JOIN movies_productioncompanies ON (productioncompanies.productioncompanyid = movies_productioncompanies.productioncompanies_id) WHERE movies_productioncompanies.movie_id = {movie_id}""")
    casts = Casts.objects.raw(f"""SELECT 1 as castID,* FROM casts WHERE casts.movie_id = {movie_id}""")

    rating_bar = {
        'one': get_row(
            f'''SELECT sum(counter) FROM (SELECT COUNT(rating) AS counter, rating FROM Movie_Ratings WHERE movieID = {movie_id} GROUP BY rating HAVING rating <= 1) AS derTable''')[
            0],
        'two': get_row(
            f'''SELECT sum(counter) FROM (SELECT COUNT(rating) AS counter, rating FROM Movie_Ratings WHERE movieID = {movie_id} GROUP BY rating HAVING rating > 1 AND rating <= 2) AS derTable''')[
            0],
        'three': get_row(
            f'''SELECT sum(counter) FROM (SELECT COUNT(rating) AS counter, rating FROM Movie_Ratings WHERE movieID = {movie_id} GROUP BY rating HAVING rating > 2 AND rating <= 3) AS derTable''')[
            0],
        'four': get_row(
            f'''SELECT sum(counter) FROM (SELECT COUNT(rating) AS counter, rating FROM Movie_Ratings WHERE movieID = {movie_id} GROUP BY rating HAVING rating > 3 AND rating <= 4) AS derTable''')[
            0],
        'five': get_row(
            f'''SELECT sum(counter) FROM (SELECT COUNT(rating) AS counter, rating FROM Movie_Ratings WHERE movieID = {movie_id} GROUP BY rating HAVING rating > 4) AS derTable''')[
            0],
        'sum': get_row(f'''SELECT COUNT(rating) FROM Movie_Ratings WHERE movieID = {movie_id}''')[0]
    }

    if request.method == 'POST':
        rating_form = MovieRatingsForm(request.POST)
        if rating_form.is_valid():
            new_rating = MovieRatings.objects.create(title=rating_form.cleaned_data['title'], description= rating_form.cleaned_data['description'],rating=rating_form.cleaned_data['rating'], movieid=movie_obj, userid=request.user, created_at=timezone.now(), updated_at=timezone.now())
            new_rating.save()
            return HttpResponseRedirect(reverse('movie_app:details', args=(movie_id,)))

        else:
            pass
    else:
        rating_form = MovieRatingsForm()
    sort_val = request.GET.get('sort_val')
    sort_types = [
        {
            'id': 'date',
            'name': 'Date'
        },
        {
            'id': 'rank',
            'name': 'Ranking'
        },
        {
            'id': 'popularity',
            'name': 'Popularity'
        }
    ]
    if sort_val == 'date':
        movie_ratings = MovieRatings.objects.filter(movieid=movie_id).order_by('updated_at')
    elif sort_val == 'rank':
        movie_ratings = MovieRatings.objects.filter(movieid=movie_id).annotate(rank=(Sum(F('up_votes')+F('down_votes')))).order_by('-rank')
    elif sort_val == 'popularity':
        movie_ratings = MovieRatings.objects.filter(movieid=movie_id).annotate(popularity=(F('up_votes')-F('down_votes'))).order_by('-popularity')
    else:
        movie_ratings = MovieRatings.objects.filter(movieid=movie_id)
    ratings_paginator = Paginator(movie_ratings, 10)  # 10 movies per page
    ratings_page = ratings_paginator.get_page(request.GET.get('page'))
    return render(request, 'movie_app/movie_details.html',
                  {'movie': movie_obj, 'genres': genres, 'production_countries': production_countries,
                   'production_companies': production_companies, 'casts': casts, 'rating_bar': rating_bar,
                   'rating_form': rating_form, 'ratings_page': ratings_page, 'sort_types': sort_types})


def movie_ratings_vote(request, rating_id, vote_value):
    obj = MovieRatings.objects.get(id=rating_id)
    if obj.userid is not request.user:
        p, created = MovieRatingsVotes.objects.get_or_create(movie_rating_id=obj, userid=request.user, defaults={'vote': vote_value})
        if created:
            if vote_value:
                obj.up_votes = obj.up_votes + 1
            elif not vote_value:
                obj.down_votes = obj.down_votes + 1
            obj.save()
        else:
            if vote_value and not p.vote:
                obj.up_votes = obj.up_votes + 1
                obj.down_votes = obj.down_votes - 1
                p.vote = True
            elif not vote_value and p.vote:
                obj.down_votes = obj.down_votes + 1
                obj.up_votes = obj.up_votes - 1
                p.vote = False
            p.save()
            obj.save()
    return redirect('movie_app:details', movie_id=obj.movieid.movieid)


class SearchResultsView(generic.ListView):
    model = Movies
    template_name = 'movie_app/movies.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Movies.objects.filter(Q(title__icontains=query))
        return object_list


def is_checked(checkbox_value):
    if not checkbox_value:
        return False
    if checkbox_value == 'on':
        return True
    else:
        return False


def search_results(request):
    movie_list = None
    search_bar = request.GET.get('q')
    adult = request.GET.get('adult')
    sort_val = request.GET.get('sort_val')
    sort_query = ''
    genre_id = request.GET.get('genre_id')
    lang_iso_639_1 = request.GET.get('lang_iso_639_1')

    if sort_val == 'pop_desc':
        sort_query = 'ORDER BY popularity DESC'
    elif sort_val == 'pop_asc':
        sort_query = 'ORDER BY popularity ASC'
    elif sort_val == 'rel_new':
        sort_query = 'AND release_date IS NOT NULL ORDER BY release_date DESC'
    elif sort_val == 'rel_old':
        sort_query = 'AND release_date IS NOT NULL ORDER BY release_date ASC'
    elif sort_val == 'rev_desc':
        sort_query = 'ORDER BY vote_count DESC'
    elif sort_val == 'rev_asc':
        sort_query = 'ORDER BY vote_count ASC'

    if search_bar:
        search_bar_query = " AND title ~ '" + str(search_bar) + "'"
    else:
        search_bar_query = ''

    if is_checked(adult):
        if genre_id:
            if lang_iso_639_1:
                movie_list = Movies.objects.raw(
                    '''SELECT adult, budget, homepage, movieid, imdb_id, original_language, original_title, overview, popularity, poster_path, release_date, revenue, runtime, status, tagline, title, video, vote_average, vote_count, created_at, updated_at FROM "movies" INNER JOIN "movies_genres" ON ("movies"."movieid" = "movies_genres"."movie_id") INNER JOIN "movies_languages" ON ("movies"."movieid" = "movies_languages"."movie_id") WHERE ("movies"."adult" = true AND "movies_genres"."genre_id" = %s AND "movies_languages"."language_id" =%s AND UPPER("movies"."title"::text) LIKE UPPER('%%')) ''' + search_bar_query + sort_query + ''' LIMIT 15''',
                    [str(genre_id), str(lang_iso_639_1)])
            else:
                movie_list = Movies.objects.raw(
                    '''SELECT adult, budget, homepage, movieid, imdb_id, original_language, original_title, overview, popularity, poster_path, release_date, revenue, runtime, status, tagline, title, video, vote_average, vote_count, created_at, updated_at FROM movies WHERE movieid IN(SELECT movie_id FROM Movies_Genres WHERE genre_id=%s) AND adult='true' ''' + search_bar_query + sort_query + ''' LIMIT 15''',
                    [str(genre_id)])

        else:
            if lang_iso_639_1:
                movie_list = Movies.objects.raw(
                    '''SELECT adult, budget, homepage, movieid, imdb_id, original_language, original_title, overview, popularity, poster_path, release_date, revenue, runtime, status, tagline, title, video, vote_average, vote_count, created_at, updated_at FROM movies WHERE movieid IN(SELECT movie_id FROM Movies_Languages WHERE language_id=%s) AND adult='true' ''' + search_bar_query + sort_query + ''' LIMIT 15''',
                    [str(lang_iso_639_1)])

            else:
                movie_list = Movies.objects.raw(
                    '''SELECT adult, budget, homepage, movieid, imdb_id, original_language, original_title, overview, popularity, poster_path, release_date, revenue, runtime, status, tagline, title, video, vote_average, vote_count, created_at, updated_at FROM movies WHERE adult='true' ''' + search_bar_query + sort_query + ''' LIMIT 15''')

    else:
        if genre_id:
            if lang_iso_639_1:
                movie_list = Movies.objects.raw(
                    '''SELECT adult, budget, homepage, movieid, imdb_id, original_language, original_title, overview, popularity, poster_path, release_date, revenue, runtime, status, tagline, title, video, vote_average, vote_count, created_at, updated_at FROM "movies" INNER JOIN "movies_genres" ON ("movies"."movieid" = "movies_genres"."movie_id") INNER JOIN "movies_languages" ON ("movies"."movieid" = "movies_languages"."movie_id") WHERE ("movies_genres"."genre_id" = %s AND "movies_languages"."language_id" =%s AND UPPER("movies"."title"::text) LIKE UPPER('%%')) ''' + search_bar_query + sort_query + ''' LIMIT 15''',
                    [str(genre_id), str(lang_iso_639_1)])
            else:
                movie_list = Movies.objects.raw(
                    '''SELECT adult, budget, homepage, movieid, imdb_id, original_language, original_title, overview, popularity, poster_path, release_date, revenue, runtime, status, tagline, title, video, vote_average, vote_count, created_at, updated_at FROM movies WHERE movieid IN(SELECT movie_id FROM Movies_Genres WHERE genre_id=%s) ''' + search_bar_query + sort_query + ''' LIMIT 15''',
                    [str(genre_id)])
        else:
            if lang_iso_639_1:
                movie_list = Movies.objects.raw(
                    '''SELECT adult, budget, homepage, movieid, imdb_id, original_language, original_title, overview, popularity, poster_path, release_date, revenue, runtime, status, tagline, title, video, vote_average, vote_count, created_at, updated_at FROM movies WHERE movieid IN(SELECT movie_id FROM Movies_Languages WHERE language_id=%s) ''' + search_bar_query + sort_query + ''' LIMIT 15''',
                    [str(lang_iso_639_1)])

            else:
                movie_list = Movies.objects.raw(
                    '''SELECT adult, budget, homepage, movieid, imdb_id, original_language, original_title, overview, popularity, poster_path, release_date, revenue, runtime, status, tagline, title, video, vote_average, vote_count, created_at, updated_at FROM movies WHERE TRUE ''' + search_bar_query + sort_query + ''' LIMIT 15''')

    genres = Genres.objects.all()
    languages = Languages.objects.all()
    sort_types = [{"name": "Popularity (most to least)", "id": "pop_desc"},
                  {"name": "Popularity (least to most)", "id": "pop_asc"},
                  {"name": "Release date (newest to oldest)", "id": "rel_new"},
                  {"name": "Release date (oldest to newest)", "id": "rel_old"},
                  {"name": "Reviews (most to least)", "id": "rev_desc"},
                  {"name": "Reviews (least to most)", "id": "rev_asc"}]

    return render(request, 'movie_app/movies.html',
                  {'page_obj': movie_list, 'genres': genres, 'languages': languages, 'sort_types': sort_types})


def dashboard(request):
    return render(request, 'movie_app/dashboard_base.html')


def dashboard_reviews(request):
    sort_val = request.GET.get('sort_val')
    sort_types = [
        {
            'id': 'date',
            'name': 'Date'
        },
        {
            'id': 'popularity',
            'name': 'Popularity'
        }
    ]
    ratings_page = None
    if sort_val == 'date':
        ratings_page = MovieRatings.objects.filter(userid=request.user).order_by('created_at')
    elif sort_val == 'popularity':
        ratings_page = MovieRatings.objects.filter(userid=request.user).annotate(popularity=(F('up_votes')-F('down_votes'))).order_by('-popularity')
    return render(request, 'movie_app/dashboard_reviews.html', {'ratings_page': ratings_page, 'sort_types': sort_types})


def dashboard_delete_review(request, review_id):
    obj = get_object_or_404(MovieRatings, id=review_id)
    obj.delete()
    return render(request, 'movie_app/dashboard_reviews.html')


def dashboard_update_review(request, review_id):
    if request.method == 'POST':
        rating_form = MovieRatingsForm(data=request.POST)
        if rating_form.is_valid():
            title = rating_form.cleaned_data['title']
            description = rating_form.cleaned_data['description']
            rating = rating_form.cleaned_data['rating']
            reviewtoupdate = MovieRatings.objects.get(id=review_id)
            reviewtoupdate.title = title
            reviewtoupdate.description = description
            reviewtoupdate.rating = rating
            reviewtoupdate.updated_at = datetime.datetime.now()
            reviewtoupdate.save()
        else:
            print(rating_form.errors)
    else:
        review_init = MovieRatings.objects.get(id=review_id)
        rating_form = MovieRatingsForm(initial=model_to_dict(review_init))
    return render(request, 'movie_app/dashboard_review_update.html', {'review_update_form': rating_form})


def dashboard_reports(request):
    """
    Report show how better or worse is one movie from another, just from slovak movies ordered by year
    :param request:
    :return:
    """
    report_list = Movies.objects.raw('''
    SELECT movieid, title, original_language, avg_rating
        FROM (
                 SELECT "movies"."movieid", "movies"."title",
                        "movies"."original_language",
                        AVG("movies"."popularity")
                        OVER (PARTITION BY "movies"."original_language"
                            ORDER BY EXTRACT('year' FROM "movies"."release_date")) AS "avg_rating"
                 FROM "movies"
             ) tmp
        WHERE original_language IN ('sk') LIMIT 50''')
    return render(request, 'movie_app/dashboard_reports.html', {'report_list': report_list})


def dashboard_settings(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm(initial=model_to_dict(request.user))
        profile_form = UserProfileInfoForm()
    return render(request, 'movie_app/dashboard_account_settings.html',
                  {'user_form': user_form,
                   'profile_form': profile_form
                   })


