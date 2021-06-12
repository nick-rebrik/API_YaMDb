from django.contrib import admin

from .models import Category, Genre, Reviews, Title


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Reviews)
admin.site.register(Title)
