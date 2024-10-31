# apps/posts/forms.py

from django import forms
from .models import Post
from apps.tags.models import Tag

# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ['title', 'content', 'cover_image', 'tags']

class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple,
        required=False
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'cover_image', 'tags']