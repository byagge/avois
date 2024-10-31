# apps/likes/admin.py

from django.contrib import admin
from .models import Like

class LikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')  # Убедитесь, что 'created_at' существует в модели

admin.site.register(Like, LikeAdmin)
