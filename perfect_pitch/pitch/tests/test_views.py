from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from pitch.models import ResumeAnalysis

User = get_user_model()


class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            name="Test User", email="test@gmail.com", password="testpass123"
        )
        self.signup_url = reverse("pitch:signup")
        self.login_url = reverse("pitch:login")
        self.homepage_url = reverse("pitch:homepage")
        self.results_url = reverse("pitch:results")

    def test_homepage_view(self):
        response = self.client.get(self.homepage_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "homepage.html")

    def test_signup_view(self):
        response = self.client.post(
            self.signup_url,
            {
                "name": "New User",
                "email": "new@gmail.com",
                "password1": "testpass123",
                "password2": "testpass123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email="new@gmail.com").exists())

    def test_login_view(self):
        response = self.client.post(
            self.login_url, {"email": "test@gmail.com", "password": "testpass123"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_results_view_authenticated(self):
        self.client.login(email="test@gmail.com", password="testpass123")
        response = self.client.get(self.results_url)
        self.assertEqual(response.status_code, 302)  # Redirects if no results

    def test_results_view_unauthenticated(self):
        response = self.client.get(self.results_url)
        self.assertEqual(response.status_code, 302)
