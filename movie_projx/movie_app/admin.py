from django.contrib import admin
from .models import UserProfileInfo, Movies


class MovieAdmin(admin.ModelAdmin):
    exclude = ('created_at', 'updated_at', 'vote_average', 'vote_count')


# Register your models here.\
admin.site.register(UserProfileInfo)
admin.site.register(Movies, MovieAdmin)
