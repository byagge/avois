# # apps/users/models.py

# from django.contrib.auth.models import AbstractUser
# from django.db import models

# class User(AbstractUser):
#     avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
#     bio = models.TextField(blank=True, null=True)
#     title = models.CharField(max_length=255, blank=True, null=True)

#     def __str__(self):
#         return self.username

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=30, blank=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, default='images/profile.jpg')
    # banner = models.ImageField(upload_to="banners/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True, default='Unknown')
    title = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now) 

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
