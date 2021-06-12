from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class MyUser(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'User'
        MODERATOR = 'Moderator'
        ADMIN = 'Admin'

    first_name = models.CharField(
        max_length=100,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name='Фамилия',
    )
    username = models.CharField(
        max_length=100,
        verbose_name='Username',
        unique=True
    )
    bio = models.TextField()
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=255,
        unique=True,
    )
    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.USER,
    )


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
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=100, verbose_name='Произведение')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, related_name="titles")
    genre = models.ManyToManyField(Genre, blank=True, related_name="titles")
    year = models.IntegerField(
        null=True, verbose_name="Год издания", db_index=True)
    description = models.CharField(max_length=300, null=True)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Reviews(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE,
                               related_name='reviews')
    score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    pub_date = models.DateField(auto_now_add=True,
                                verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.CheckConstraint(
                check=models.Q(score__range=(0, 10)), name='valid_rate'
            ),
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'),
        ]

    def __str__(self):
        return f'{self.text[:50]}...'


class Comments(models.Model):
    review = models.ForeignKey(Reviews, on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE,
                               related_name='comments')
    pub_date = models.DateField(auto_now_add=True,
                                verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
