from django.urls import path
from . import views

app_name = "pitch"

urlpatterns = [
    path("", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("homepage/", views.homepage, name="homepage"),
]
