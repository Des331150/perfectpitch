from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import Login_view, SignupView, HomepageView, ResultsView

app_name = "pitch"

urlpatterns = [
    path("", HomepageView.as_view(), name="homepage"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", Login_view.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="pitch:homepage"), name="logout"),
    path("results/", ResultsView.as_view(), name="results"),
]
