from . import views
from django.urls import path
from .views import Login_view, SignupView

app_name = "pitch"

urlpatterns = [
    path("", Login_view.as_view(), name="login"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("homepage/", views.homepage, name="homepage"),
]
