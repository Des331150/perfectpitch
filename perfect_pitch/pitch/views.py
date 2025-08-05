from django.shortcuts import render
from django.views.generic import CreateView
from .models import CustomUser


# Create your views here.
class SignupView(CreateView):
    model = CustomUser


def signup(request):
    return render(request, "signup.html")


def homepage(request):
    return render(request, "homepage.html")
