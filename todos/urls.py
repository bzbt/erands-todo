from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("account/", include("django.contrib.auth.urls")),
    path("signup/", views.signup, name="signup"),
]
