# apps/tags/views.py

from django.shortcuts import render, get_object_or_404
from .models import Tag
from apps.posts.models import Post

def posts_by_tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    posts = Post.objects.filter(tags=tag)
    return render(request, 'tags/posts_by_tag.html', {'tag': tag, 'posts': posts})
