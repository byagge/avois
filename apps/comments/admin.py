from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'text', 'created_at')  # Ensure 'user' is included here

admin.site.register(Comment, CommentAdmin)