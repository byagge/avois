# apps/likes/models.py

from django.db import models
from apps.posts.models import Post
from apps.users.models import User

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')  # Изменено related_name
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} likes {self.post}'
