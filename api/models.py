from django.db import models


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
