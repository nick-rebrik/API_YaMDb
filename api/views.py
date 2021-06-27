from django.conf import settings
from django.contrib.auth.tokens import default_token_generator as token
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .filter import TitleFilter
from .models import Category, Genre, MyUser, Review, Title
from .permissions import IsAdmin, IsAdminOrModerator, IsSafeMethodOrIsAdmin
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, TokenSerializer,
                          ReviewSerializer, SendEmailSerializer,
                          TitleCreateSerializer, TitleListSerializer,
                          UserSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrModerator, ]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrModerator, ]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        serializer.save(author=self.request.user, review=review)


class CustomMixin(CreateModelMixin,
                  ListModelMixin,
                  DestroyModelMixin,
                  viewsets.GenericViewSet):
    pass


class CategoryViewSet(CustomMixin):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ['name']
    lookup_field = 'slug'
    permission_classes = [IsSafeMethodOrIsAdmin, ]


class GenreViewSet(CustomMixin):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ['name']
    lookup_field = 'slug'
    permission_classes = [IsSafeMethodOrIsAdmin, ]


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('id')
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = TitleFilter
    permission_classes = [IsSafeMethodOrIsAdmin, ]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleCreateSerializer
        return TitleListSerializer


class MyTokenObtainView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, created = MyUser.objects.get_or_create(
            email=request.data['email'])
        if not token.check_token(user, request.data['confirmation code']):
            raise AuthenticationFailed()
        refresh = RefreshToken.for_user(user)
        return Response('token: ' + str(refresh.access_token),
                        status=status.HTTP_200_OK)


class SendEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SendEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = self.request.data['email']
        user = get_object_or_404(MyUser, email=email)
        confirmation_code = token.make_token(user)
        send_mail(
            'Confirmation code email',
            'confirmation code: {}'.format(confirmation_code),
            settings.DOMAIN_NAME,
            [email],
            fail_silently=False,
        )
        return Response(
            f'Код подтверждения отправлен на почту {email}',
            status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    permission_classes = [IsAuthenticated, IsAdmin]

    @action(detail=False,
            methods=['get', 'patch'],
            permission_classes=[IsAuthenticated],
            url_name='me')
    def me(self, request):
        if self.request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        serializer = self.get_serializer(request.user,
                                         data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)
