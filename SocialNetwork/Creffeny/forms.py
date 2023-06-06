from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


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


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Username'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Password'
            })
        }
