from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Category, Comment, Genre, MyUser, Review, Title

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

    class Meta:
        fields = ['id', 'text', 'author', 'score', 'pub_date']
        model = Review
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Review.objects.all(),
        #         fields=['title', 'author']
        #     )
        # ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ['id', 'text', 'author', 'pub_date']
        model = Comment


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False
        self.fields['confirmation code'] = serializers.CharField()

    def validate(self, attrs):
        attrs.update({'password': attrs['confirmation code']})
        return super().validate(attrs)


class SendEmailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('email',)
        model = MyUser


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(default=None)
    last_name = serializers.CharField(default=None)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=MyUser.objects.all())]
    )
    bio = serializers.CharField(default=None)
    role = serializers.ChoiceField(
        default='user',
        choices=MyUser.Roles
    )

    class Meta:
        model = MyUser
        exclude = ('password',)
        # lookup_field = 'username'
