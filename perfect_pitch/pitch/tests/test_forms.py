from django.test import TestCase
from django.contrib.auth import get_user_model
from pitch.forms import UserRegistrationForm, UserLoginForm, ResumeAnalysisForm
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


class UserRegistrationFormTest(TestCase):
    def test_form_with_valid_data(self):
        form_data = {
            "name": "John Doe",
            "email": "johndoe@gmail.com",
            "password1": "hotflame02",
            "password2": "hotflame02",
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_with_missing_fields(self):
        form_data = {
            "name": "",
            "email": "",
            "password1": "hotflame02",
            "password2": "hotflame02",
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_with_password_mismatch(self):
        form_data = {
            "name": "John Doe",
            "email": "johndoe@gmail.com",
            "password1": "hotflame02",
            "password2": "hotkink99",
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_duplicate_email(self):
        # Create a user first
        User.objects.create_user(
            name="Existing User", email="existing@gmail.com", password="testpass123"
        )
        # Try to create another user with same email
        form_data = {
            "name": "New User",
            "email": "existing@gmail.com",
            "password1": "hotflame02",
            "password2": "hotflame02",
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())


class UserLoginFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            name="Test User", email="test@gmail.com", password="hotflame02"
        )

    def test_with_valid_credentials(self):
        form_data = {
            "email": "test@gmail.com",
            "password": "hotflame02",
        }
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_with_invalid_password(self):
        form_data = {
            "email": "test@gmail.com",
            "password": "wrongpassword",
        }
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_with_nonexistent_email(self):
        form_data = {
            "email": "nonexistent@gmail.com",
            "password": "hotflame02",
        }
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_with_empty_fields(self):
        form_data = {"email": "", "password": ""}
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())


class ResumeAnalysisFormTest(TestCase):
    def setUp(self):
        # Create a simple PDF file in memory
        self.pdf_content = b"%PDF-1.4 This is a test PDF file"
        self.pdf_file = SimpleUploadedFile(
            name="test_resume.pdf",
            content=self.pdf_content,
            content_type="application/pdf",
        )

        self.docx_content = b"This is a fake DOCX file"
        self.docx_file = SimpleUploadedFile(
            name="test_resume.docx",
            content=self.docx_content,
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    def test_valid_pdf_upload(self):
        form_data = {
            "job_title": "Software Engineer",
            "job_description": "Test job description",
        }
        file_data = {"resume_file": self.pdf_file}
        form = ResumeAnalysisForm(data=form_data, files=file_data)
        self.assertTrue(form.is_valid())

    def test_invalid_file_type(self):
        form_data = {
            "job_title": "Software Engineer",
            "job_description": "Test job description",
        }
        file_data = {"resume_file": self.docx_file}
        form = ResumeAnalysisForm(data=form_data, files=file_data)
        self.assertFalse(form.is_valid())
