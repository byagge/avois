# project_name/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('apps.main.urls')),
    path('users/', include('apps.users.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('', include('apps.posts.urls')),
    path('comments/', include('apps.comments.urls')),
    path('notifications/', include('apps.notifications.urls')),
]
