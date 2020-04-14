import datetime

from django import forms
from django.contrib.auth.models import User
from django.forms import SelectDateWidget

from .models import UserProfileInfo, Movies


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
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