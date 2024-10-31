# apps/posts/urls.py

from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import post_list, post_detail, create_post, like_post, homepage, retrieve, weather_view, my_posts, edit_post, delete_post
# from apps.comments.views import add_comment

urlpatterns = [
    path('', homepage, name='homepage'),
    path('retrieve/<int:pk>', retrieve, name='retrieve'),
    path('header/', weather_view, name='header'),
    path('create/', create_post, name='create_post'),
    path('myposts', my_posts, name='myposts'),
    path('edit-post/<int:post_id>/', edit_post, name='edit_post'),
    path('delete-post/<int:post_id>/', delete_post, name='delete_post'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)