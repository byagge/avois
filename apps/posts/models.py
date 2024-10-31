# # apps/posts/models.py

# from django.db import models
# from apps.users.models import User

# class Post(models.Model):
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     content = models.TextField()
#     cover_image = models.ImageField(upload_to="cover_images", blank=True, null=True)
#     tags = models.ManyToManyField('tags.Tag', related_name="tagged_posts")
#     likes = models.ManyToManyField(User, through='likes.Like', related_name="liked_posts")
    
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# apps/posts/models.py

from django.db import models
from apps.users.models import User

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    cover_image = models.ImageField(upload_to='images/', blank=True, null=True)
    tags = models.ManyToManyField('tags.Tag', related_name="tagged_posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Убедитесь, что это related_name уникально
    likes = models.ManyToManyField(User, through='likes.Like', related_name='liked_posts')
