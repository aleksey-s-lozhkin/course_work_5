from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from .views import (
    RegisterView,
    CustomTokenObtainPairView,
    UserProfileView,
    LogoutView,
    CheckEmailView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),

    path('profile/', UserProfileView.as_view(), name='profile'),

    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('logout/', LogoutView.as_view(), name='logout'),

    path('check-email/', CheckEmailView.as_view(), name='check_email'),
]