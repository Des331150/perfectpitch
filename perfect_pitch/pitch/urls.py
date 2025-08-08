from . import views
from django.urls import path
from .views import Login_view, SignupView, HomepageView

app_name = "pitch"

urlpatterns = [
    path("", HomepageView.as_view(), name="homepage"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", Login_view.as_view(), name="login"),
    path("results/", views.results, name="results"),
]
