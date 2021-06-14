from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from api.views import MyTokenObtainView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/token', MyTokenObtainView.as_view(),
    name='obtain_token'),
    path('api/', include('api.urls')),
    path('redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
