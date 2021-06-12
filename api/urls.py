from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, ReviewViewSet

router_v1 = DefaultRouter()
router_v1.register(
    r'titles/(?P<id>\d+)/reviews', ReviewViewSet, basename='Review'
)
router_v1.register(
    r'titles/(?P<id>\d+)/reviews/(?P<id>\d+)/comments',
    CommentViewSet, basename='Comment'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
