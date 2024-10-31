# apps/users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'avatar', 'bio', 'title']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'username', 'email', 'name', 'bio', 'title']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }
