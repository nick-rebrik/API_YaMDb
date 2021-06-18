# import function for password encyption
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase

from .filter import TitleFilter
from .models import Category, Genre, MyUser, Review, Title
from .permissions import IsAdmin, IsAdminOrModerator, IsSafeMethodOrIsAdmin
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, MyTokenObtainPairSerializer,
                          ReviewSerializer, SendEmailSerializer,
                          TitleCreateSerializer, TitleListSerializer)
from .serializers import (UserSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminOrModerator]
        return [permission() for permission in permission_classes]

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

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminOrModerator]
        return [permission() for permission in permission_classes]


class CustomMixin(CreateModelMixin, ListModelMixin, DestroyModelMixin,
                  viewsets.GenericViewSet):
    # так тоже должно работать
    pass


class CategoryViewSet(CustomMixin):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ['name']
    lookup_field = 'slug'

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsSafeMethodOrIsAdmin]
        return [permission() for permission in permission_classes]


class GenreViewSet(CustomMixin):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter,)
    search_fields = ['name']
    lookup_field = 'slug'

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsSafeMethodOrIsAdmin]
        return [permission() for permission in permission_classes]


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('id')
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleCreateSerializer
        return TitleListSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsSafeMethodOrIsAdmin]
        return [permission() for permission in permission_classes]


class MyTokenObtainView(TokenViewBase):
    serializer_class = MyTokenObtainPairSerializer


class SendEmailView(APIView):
    def post(self, request, format=None):
        serializer = SendEmailSerializer(data=request.data)
        if serializer.is_valid():
            confirmation_code = MyUser.objects.make_random_password()

            serializer.save(
                email=self.request.data['email'],
                password=make_password(confirmation_code),
            )

            send_mail(
                'Confirmation code email',
                'confirmation code: {}'.format(confirmation_code),
                'from@example.com',
                [self.request.data['email']],
                fail_silently=False,
            )
            return Response(serializer.validated_data,
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    # filter_backends = (SearchFilter,)
    # search_fields = ['username']
    lookup_field = "username"
    permission_classes = [IsAuthenticated, IsAdmin]

    @action(detail=False,
            methods=['get', 'patch'],
            permission_classes=[IsAuthenticated],
            url_name='me')
    def me(self, request):
        me = get_object_or_404(MyUser, id=self.request.user.id)
        if self.request.method == 'GET':
            serializer = self.get_serializer(me)
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(me,
                                             data=request.data, partial=True)
            if serializer.is_valid():
                self.perform_update(serializer)
                return Response(serializer.data,
                                status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
