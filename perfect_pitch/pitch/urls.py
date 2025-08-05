from . import views
from django.urls import path
from .views import LoginView, SignupView

app_name = "pitch"

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("homepage/", views.homepage, name="homepage"),
]
