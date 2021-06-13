from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.views import TokenViewBase

from .filter import TitleFilter
from .models import Category, Genre, Title
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, MyTokenObtainPairSerializer,
                          ReviewSerializer, TitleCreateSerializer,
                          TitleListSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['id'])
        serializer.save(author=self.request.user, title=title)


class CustomMixin(CreateModelMixin, ListModelMixin, DestroyModelMixin,
                  viewsets.GenericViewSet):
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class CategoryViewSet(CustomMixin):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    search_fields = ['name']
    lookup_field = 'slug'



class GenreViewSet(CustomMixin):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    search_fields = ['name']
    lookup_field = 'slug'


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

class MyTokenObtainView(TokenViewBase):
    serializer_class = MyTokenObtainPairSerializer
