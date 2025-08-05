from django import forms, UserCreationForm, ValidationError
from .models import CustomUser
from django.contrib.auth import authenticate
import os


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["name", "email", "password1", "password2"]


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)

        if user is None:
            raise forms.ValidationError("Invalid email or password.")

        self.user = user


class ResumeAnalysisForm(forms.Form):
    resume_file = forms.FileField()
    job_title = forms.CharField()

    def clean_resume_file(self):
        resume = self.cleaned_data["resume_file"]
        extension = os.path.splitext(resume.name)
        allowed_extensions = [".pdf"]

        if extension.lower() not in allowed_extensions:
            raise ValidationError("Only PDF files are allowed")
        return resume
