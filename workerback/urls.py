from django.contrib import admin
from django.urls import path, include
from api.views import RegisterView, LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', LoginView.as_view(), name='rest_login'),  # Custom login view
    path('api/auth/', include('dj_rest_auth.urls')),  # Other auth endpoints
    path('api/auth/registration/', RegisterView.as_view(), name='rest_register'),
    path('accounts/', include('allauth.urls')),
]