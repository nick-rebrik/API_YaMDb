from django.contrib import admin

from .models import Category, Genre, Reviews, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'category', 'genre', 'year')
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Reviews)
admin.site.register(Title, TitleAdmin)
