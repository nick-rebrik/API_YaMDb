from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class MyUser(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()
    is_active = True
    is_superuser = models.BooleanField(
        default=False)
    is_staff = models.BooleanField(
        default=False)
    date_joined = models.DateTimeField(
        default=timezone.now,
        null=True)
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

    class Meta:
        ordering = ['id']


class ConfCode(models.Model):
    confcode = models.CharField(max_length=128)
    email = models.CharField(max_length=200)


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
    year = models.IntegerField(verbose_name="Год издания", db_index=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 blank=True, null=True, related_name="titles")
    genre = models.ManyToManyField(Genre, related_name="titles")
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
            models.CheckConstraint(
                check=models.Q(score__range=(0, 10)), name='valid_rate'
            ),
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
