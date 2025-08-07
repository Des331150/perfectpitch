from django.shortcuts import render
from django.views.generic import CreateView, FormView
from .models import CustomUser
from .forms import UserRegistrationForm, UserLoginForm, ResumeAnalysisForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import login


# Create your views here.
class SignupView(CreateView):
    model = CustomUser
    form_class = UserRegistrationForm
    template_name = "signup.html"
    success_url = reverse_lazy("login")


class Login_view(LoginView):
    def post(self, request, *args, **kwargs):
        print("POST received")
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        print("GET received")
        return super().get(request, *args, **kwargs)

    authentication_form = UserLoginForm
    template_name = "login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("homepage")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if "request" in kwargs:
            kwargs.pop("request")
        return kwargs

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)


class HomepageView(FormView):
    form_class = ResumeAnalysisForm
    template_name = "homepage.html"
    success_url = reverse_lazy("results")


def results(request):
    return render(request, "results.html")
