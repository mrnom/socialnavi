from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    username = models.CharField(max_length=150, blank=True, null=True)

    email = models.EmailField(unique=True)

    bio = models.TextField(blank=True, null=True)

    site = models.URLField(blank=True, null=True)

    avatar = models.URLField(blank=True, null=True)

    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')
