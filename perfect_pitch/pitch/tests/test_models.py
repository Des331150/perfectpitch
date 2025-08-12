from django.test import TestCase
from django.contrib.auth import get_user_model
from pitch.models import ResumeAnalysis
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            name="Test User", email="test@gmail.com", password="testpass123"
        )
        self.assertEqual(user.email, "test@gmail.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            name="Admin User", email="admin@gmail.com", password="testpass123"
        )
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class ResumeAnalysisModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            name="Test User", email="test@gmail.com", password="testpass123"
        )
        self.pdf_content = b"Fake PDF content"
        self.resume = SimpleUploadedFile(
            "test.pdf", self.pdf_content, content_type="application/pdf"
        )

    def test_create_analysis(self):
        analysis = ResumeAnalysis.objects.create(
            user=self.user,
            resume_file=self.resume,
            job_title="Software Engineer",
            job_description="Test description",
            score=85,
        )
        self.assertEqual(analysis.user, self.user)
        self.assertEqual(analysis.score, 85)
