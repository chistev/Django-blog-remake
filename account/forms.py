from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': "Enter your username"
            }),
            'password1': forms.PasswordInput(attrs={
                'placeholder': '••••••••',
            }),
            'password2': forms.PasswordInput(attrs={
                 'placeholder': '••••••••',
            })
        }
        