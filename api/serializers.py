from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueValidator

from .auth import MyBackend
from .models import Category, Comment, ConfCode, Genre, MyUser, Roles, Review, Title

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
        if self.context['request'].method == 'POST' and (
                Review.objects.filter(
                    title_id=self.context['view'].kwargs['title_id'],
                    author=self.context['request'].user
                ).exists()
        ):
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


class MyTokenObtainPairSerializer(serializers.Serializer):
    username_field = get_user_model().USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['confirmation code'] = serializers.CharField()

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'confcode': attrs['confirmation code'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass
        backend = MyBackend()
        user = backend.authenticate(**authenticate_kwargs)
        data = {}
        if user:
            refresh = RefreshToken.for_user(user)
            data['token'] = str(refresh.access_token)
        return data


class SendEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if ConfCode.objects.filter(email=value).exists():
            raise ValidationError(
                'Вы уже получили код. Ищите в почте.'
            )

    class Meta:
        fields = ('email',)
        model = ConfCode


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(default=None)
    last_name = serializers.CharField(default=None)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=MyUser.objects.all())]
    )
    bio = serializers.CharField(default=None)
    role = serializers.ChoiceField(
        default='user',
        choices=Roles,
    )

    class Meta:
        model = MyUser
        exclude = ('password',)
