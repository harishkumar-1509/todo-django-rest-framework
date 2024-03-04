from django.urls import path
from ..api.views import *

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name="register-user"),
    path('login/', UserLoginView.as_view(), name="login-user"),
    path('profile/', UserProfileView.as_view(), name="user-profile"),
    path('changepassword/', UserChangePasswordView.as_view(), name="user-change-password")
]