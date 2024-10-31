from django.db import models
from apps.users.models import User  # Ensure you import User
from apps.posts.models import Post  # Adjust the import based on your project structure

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # This field should exist
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text  # Optional: to represent the comment by its text