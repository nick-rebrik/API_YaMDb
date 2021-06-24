from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, CommentViewSet, GenreViewSet, \
    MyTokenObtainView, ReviewViewSet, SendEmailView, TitlesViewSet, UserViewSet

router_v1 = DefaultRouter()
router_v1.register("users", UserViewSet, basename='User')

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
    path('v1/auth/email/', SendEmailView.as_view(),
         name='obtain_confirmation_code'),
    path('v1/auth/token/', MyTokenObtainView.as_view(),
         name='obtain_token'),
]
