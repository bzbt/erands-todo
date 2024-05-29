from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy(settings.SIGNUP_REDIRECT_URL)
    template_name = "registration/signup.html"
