from django.shortcuts import render
from django.views.generic import CreateView
from .models import CustomUser
from .forms import UserRegistrationForm, UserLoginForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView as DjangoLoginView


# Create your views here.
class SignupView(CreateView):
    model = CustomUser
    form_class = UserRegistrationForm
    template_name = "signup.html"
    success_url = reverse_lazy("login")


class LoginView(DjangoLoginView):
    authentication_form = UserLoginForm
    template_name = "login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("homepage")


def homepage(request):
    return render(request, "homepage.html")
