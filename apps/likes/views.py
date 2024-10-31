from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from posts.models import Post
from .models import Like
from django.db import IntegrityError
from django.contrib import messages

@login_required
def add_like(request, post_id):
    try:
        post = get_object_or_404(Post, id=post_id)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()  # Если уже существует, удаляем (аналог дизлайка)
    except IntegrityError:
        messages.error(request, "Ошибка с добавлением лайка.")
        return redirect('post_detail', pk=post_id)
    return redirect('post_detail', pk=post_id)
