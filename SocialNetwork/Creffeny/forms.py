from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import FileExtensionValidator

from Creffeny.models import Post


class Registration(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email'
            }),
            'password1': forms.PasswordInput(attrs={
                'placeholder': 'Password'
            }),
            'password2': forms.PasswordInput(attrs={
                'placeholder': 'Confirm Password'
            })
        }


class PostForm(forms.Form):
    title = forms.CharField(max_length=100)
    image = forms.FileField()
    body = forms.CharField(max_length=1250)
