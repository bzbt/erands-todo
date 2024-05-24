from django.contrib.auth.decorators import login_required
from django.forms import Form
from django.shortcuts import render


# Index page of the app
@login_required(login_url="account/login/")
def index(request):
    return render(request, "todo/home.html")


def signup(request):
    return render(
        request,
        "registration/signup.html",
        {"form": Form()},
    )
