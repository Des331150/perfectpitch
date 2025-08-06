from django.shortcuts import render
from django.views.generic import CreateView
from .models import CustomUser
from .forms import UserRegistrationForm, UserLoginForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView


# Create your views here.
class SignupView(CreateView):
    model = CustomUser
    form_class = UserRegistrationForm
    template_name = "signup.html"
    success_url = reverse_lazy("login")


class Login_view(LoginView):
    authentication_form = UserLoginForm
    template_name = "login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("homepage")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if "request" in kwargs:
            kwargs.pop("request")
        return kwargs


def homepage(request):
    return render(request, "homepage.html")


def results(request):
    return render(
        request,
        "results.html",
    )
