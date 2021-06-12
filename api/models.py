from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    
    class Roles(models.TextChoices):
        USER = 'User'
        MODERATOR = 'Moderator'
        ADMIN = 'Admin'

    first_name = models.CharField(
        max_length=100,
        verbose_name = 'Имя',
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name = 'Фамилия',
    )
    username = models.CharField(
        max_length=100,
        verbose_name = 'Username',
        unique = True
    )
    bio = models.TextField()
    email = models.EmailField(
        verbose_name= 'Адрес электронной почты',
        max_length=255,
        unique=True,
    )
    role = models.CharField(
        max_length = 20,
        choices = Roles.choices,
        default = Roles.USER,
    )

