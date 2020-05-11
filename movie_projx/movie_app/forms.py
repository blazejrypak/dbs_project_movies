import datetime

from django import forms
from django.contrib.auth.models import User
from django.forms import SelectDateWidget

from .models import UserProfileInfo, MovieRatings


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password', 'email')


class UserProfileInfoForm(forms.ModelForm):
    birth_date = forms.DateField(widget=SelectDateWidget(
        empty_label=("Choose Year", "Choose Month", "Choose Day"),
        years=range(1980, datetime.date.today().year+1)
    ),)
    class Meta:
        model = UserProfileInfo
        fields = ('birth_date', )


class MovieRatingsForm(forms.ModelForm):
    title = forms.CharField()
    rating = forms.ChoiceField(choices=(('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')))
    description = forms.CharField(label='Description', max_length=500)

    class Meta:
        model = MovieRatings
        fields = ('title', 'rating', 'description')
