from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from .models import (Category, Comment, Genre, MyUser, Review, Roles, Title)

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'


class TitleListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    def validate(self, attrs):
        if self.context['request'].method != 'POST':
            return attrs
        if Review.objects.filter(
            title_id=self.context['view'].kwargs['title_id'],
            author=self.context['request'].user
        ).exists():
            raise ValidationError(
                'Вы уже оставили отзыв на данное произведение'
            )
        return attrs

    class Meta:
        fields = ['id', 'text', 'author', 'score', 'pub_date']
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ['id', 'text', 'author', 'pub_date']
        model = Comment


class TokenSerializer(serializers.Serializer):
    username_field = get_user_model().USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.EmailField()
        self.fields['confirmation code'] = serializers.CharField()


class SendEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        fields = ('email',)
        model = User


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(default=None)
    last_name = serializers.CharField(default=None)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=MyUser.objects.all())]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=MyUser.objects.all())]
    )
    bio = serializers.CharField(default=None)
    role = serializers.ChoiceField(
        default=Roles.USER,
        choices=Roles,
    )

    class Meta:
        fields = ['first_name', 'last_name',
                  'email', 'username', 'bio', 'role']
        model = MyUser
