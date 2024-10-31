# apps/posts/models.py

from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    cover_image_url = models.URLField(blank=True, null=True)  # поле для хранения URL обложки

    def __str__(self):
        return self.title
