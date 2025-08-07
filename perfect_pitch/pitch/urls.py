from . import views
from django.urls import path
from .views import Login_view, SignupView, HomepageView

app_name = "pitch"

urlpatterns = [
    path("", Login_view.as_view(), name="login"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("homepage/", HomepageView.as_view(), name="homepage"),
    path("results/", views.results, name="results"),
]
