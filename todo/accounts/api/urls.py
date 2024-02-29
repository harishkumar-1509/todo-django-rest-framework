from django.urls import path
from ..api.views import *

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name="register-user"),
    path('login/', UserLoginView.as_view(), name="login-user")
]