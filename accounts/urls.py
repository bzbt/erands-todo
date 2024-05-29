from django.contrib.auth.views import LogoutView
from django.urls import path, include

from .views import SignUpView


urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
