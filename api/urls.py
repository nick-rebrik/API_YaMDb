from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, ReviewViewSet, TitlesViewSet, GenreViewSet, \
    CategoryViewSet, SendEmailView, MyTokenObtainView

router_v1 = DefaultRouter()
router_v1.register("titles", TitlesViewSet, basename='Title')
router_v1.register("genres", GenreViewSet, basename='Genre')
router_v1.register("categories", CategoryViewSet, basename='Category')
router_v1.register(
    r'titles/(?P<title_id>[0-9]+)/reviews', ReviewViewSet, basename='Review'
)
router_v1.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='Comment'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('auth/email/', SendEmailView.as_view(),
    name ='obtain_confirmation_code'),
    path('auth/token/', MyTokenObtainView.as_view(),
    name='obtain_token'),
]
