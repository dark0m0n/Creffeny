from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import FileExtensionValidator

from Creffeny.models import Post


class Registration(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class PostForm(forms.Form):
    title = forms.CharField(max_length=100)
    image = forms.FileField()
    body = forms.CharField(max_length=1250)
