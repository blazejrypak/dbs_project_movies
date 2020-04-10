from django.contrib import admin
from django.contrib.admin import StackedInline, ModelAdmin
from .models import *


class GenresInline(admin.TabularInline):
    model = MoviesGenres
    extra = 1


class ProductionCountryInline(admin.TabularInline):
    model = MoviesProductioncountries
    extra = 1


class ProductionCompanyInline(admin.TabularInline):
    model = MoviesProductioncompanies
    extra = 1

class LanguagesInline(admin.TabularInline):
    model = MoviesLanguages
    extra = 1

class CastsInline(admin.StackedInline):
    model = Casts
    extra = 1

class MovieAdmin(admin.ModelAdmin):
    exclude = ('created_at', 'updated_at', 'vote_average', 'vote_count')
    inlines = [GenresInline, LanguagesInline, ProductionCountryInline, CastsInline]


# Register your models here.\
admin.site.register(UserProfileInfo)
admin.site.register(Movies, MovieAdmin)
