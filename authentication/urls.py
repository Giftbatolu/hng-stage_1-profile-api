from django.urls import path
from .views import github_login, github_callback
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('github/login/', github_login, name='github_login'),
    path('github/callback/', github_callback, name='github_callback'),
]