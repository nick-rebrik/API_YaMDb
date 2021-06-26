from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validator_year


class Roles(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class MyUser(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    first_name = models.CharField(
        max_length=100,
        verbose_name='First name',
        null=True)
    last_name = models.CharField(
        max_length=100,
        verbose_name='Last name',
        null=True)
    username = models.CharField(
        max_length=100,
        verbose_name='Username',
        unique=True
    )
    bio = models.TextField(null=True)
    email = models.EmailField(
        verbose_name='email',
        unique=True
    )
    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.USER,
    )

    @property
    def is_admin(self):
        return (self.role == Roles.ADMIN or self.is_superuser
                or self.is_staff)

    @property
    def is_moderator(self):
        return self.role == Roles.MODERATOR

    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['email'],
                name='unique_email'),
        ]


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name='Жанр', unique=True)
    slug = models.SlugField(max_length=30, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Категория',
                            unique=True)
    slug = models.SlugField(max_length=30, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=100, verbose_name='Произведение')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 blank=True, null=True, related_name="titles")
    genre = models.ManyToManyField(Genre, related_name="titles")
    year = models.IntegerField(
        verbose_name="Год издания", db_index=True,
        validators=[validator_year]
    )

    description = models.CharField(max_length=300, null=True)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(1, message='Минимальная оценка - 1'),
            MaxValueValidator(10, message='Максимальная оценка - 10')
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации', db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'),
        ]

    def __str__(self):
        return self.text[:50]


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='comments'

    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации', db_index=True
    )

    def __str__(self):
        return self.text[:50]

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['id']
