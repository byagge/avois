# apps/likes/urls.py

from django.urls import path
from .views import LikePostView, UnlikePostView

urlpatterns = [
    path('like/<int:post_id>/', LikePostView, name='like-post'),
    path('unlike/<int:post_id>/', UnlikePostView, name='unlike-post'),
]
