from django.contrib.auth.models import AbstractUser
from django.db import models


class Roles(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class YamUser(AbstractUser):
    email = models.EmailField('email address', unique=True)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(
        max_length=200,
        default=Roles.USER,
        choices=Roles.choices,
    )
