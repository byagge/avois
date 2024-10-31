# apps/users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    path('logout/', views.custom_logout_view, name='logout'),
]
