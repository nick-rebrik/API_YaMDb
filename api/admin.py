from django.contrib import admin

from .models import Category, Genre, Review, Title, Comment, MyUser


@admin.register(MyUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ( 
        'username', 
        'bio', 
        'email', 
        'role')
    search_fields = ('first name','last name','username')
    list_filter = ('role',)
    empty_value_display = '-пусто-'

admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Title)
admin.site.register(Comment)
