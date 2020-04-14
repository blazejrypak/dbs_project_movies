from django.contrib import admin
from django.contrib.admin import StackedInline, ModelAdmin
from .models import *

class GenreAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

class GenresInline(admin.StackedInline):
    model = MoviesGenres
    autocomplete_fields = ['genre']
    extra = 1

class ProductionCountryAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

class ProductionCountryInline(admin.TabularInline):
    model = MoviesProductioncountries
    autocomplete_fields = ['productioncountry_iso']
    extra = 1

class ProductionCompanyAdmin(admin.ModelAdmin):
    search_fields = ['name']

class ProductionCompanyInline(admin.TabularInline):
    model = MoviesProductioncompanies
    autocomplete_fields = ['productioncompanies']
    extra = 1

class LanguagesAdmin(admin.ModelAdmin):
    search_fields = ['name']

class LanguagesInline(admin.TabularInline):
    model = MoviesLanguages
    extra = 1

class CastsInline(admin.StackedInline):
    model = Casts
    extra = 1

class MovieAdmin(admin.ModelAdmin):
    exclude = ('created_at', 'updated_at', 'vote_average', 'vote_count', 'imdb_id', 'popularity', 'poster_path', 'revenue', 'status')
    search_fields = ('original_title', 'title',)
    inlines = [GenresInline, LanguagesInline, ProductionCountryInline, ProductionCompanyInline, CastsInline]


# Register your models here.\
admin.site.register(UserProfileInfo)
admin.site.register(Genres, GenreAdmin)
admin.site.register(Languages, LanguagesAdmin)
admin.site.register(Productioncountries, ProductionCountryAdmin)
admin.site.register(Productioncompanies, ProductionCompanyAdmin)
admin.site.register(Movies, MovieAdmin)
