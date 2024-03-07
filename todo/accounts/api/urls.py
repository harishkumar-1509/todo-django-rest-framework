from django.urls import path
from ..api.views import *

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name="register-user"),
    path('login/', UserLoginView.as_view(), name="login-user"),
    path('get-access-token-from-refresh-token/', RefreshTokenView.as_view(), name="get-access-token-from-refresh-token"),
    path('profile/', UserProfileView.as_view(), name="user-profile"),
    path('change-password/', UserChangePasswordView.as_view(), name="user-change-password"),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name="send-reset-password-email"),
    path('reset-password/<uid>/<token>/', SendPasswordResetEmailView.as_view(), name="reset-password")
]