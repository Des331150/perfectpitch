from django.contrib.auth.forms import (
    forms,
    UserCreationForm,
    ValidationError,
)
from .models import CustomUser, ResumeAnalysis
from django.contrib.auth import authenticate
import os


class UserRegistrationForm(UserCreationForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "block w-full pl-10 rounded-lg border-0 bg-gray-700 text-white px-3 py-2 shadow-sm ring-1 ring-inset ring-gray-600 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-500 sm:text-sm",
                "placeholder": "Enter your full name",
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "block w-full pl-10 rounded-lg border-0 bg-gray-700 text-white px-3 py-2 shadow-sm ring-1 ring-inset ring-gray-600 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-500 sm:text-sm",
                "placeholder": "you@example.com",
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "block w-full pl-10 rounded-lg border-0 bg-gray-700 text-white px-3 py-2 shadow-sm ring-1 ring-inset ring-gray-600 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-500 sm:text-sm",
                "placeholder": "Create a password",
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "block w-full pl-10 rounded-lg border-0 bg-gray-700 text-white px-3 py-2 shadow-sm ring-1 ring-inset ring-gray-600 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-500 sm:text-sm",
                "placeholder": "Confirm password",
            }
        )
    )

    class Meta:
        model = CustomUser
        fields = ["name", "email", "password1", "password2"]


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "block w-full rounded-lg border-0 bg-gray-700 text-white px-3 py-2 shadow-sm ring-1 ring-inset ring-gray-600 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-500 sm:text-sm",
                "placeholder": "you@example.com",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "block w-full rounded-lg border-0 bg-gray-700 text-white px-3 py-2 shadow-sm ring-1 ring-inset ring-gray-600 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-500 sm:text-sm",
                "placeholder": "Enter your password",
            }
        )
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        self.user_cache = None

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Invalid email or password.")

        return cleaned_data

    def get_user(self):
        return self.user_cache


class ResumeAnalysisForm(forms.ModelForm):
    job_title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "block w-full rounded-lg border-0 bg-gray-700 text-white px-3 py-2 shadow-sm ring-1 ring-inset ring-gray-600 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-500 sm:text-sm",
                "placeholder": "Enter the job title",
            }
        )
    )
    job_description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "block w-full rounded-lg border-0 bg-gray-700 text-white px-3 py-2 shadow-sm ring-1 ring-inset ring-gray-600 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-500 sm:text-sm",
                "placeholder": "Paste the job description here",
                "rows": 4,
            }
        )
    )
    resume_file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "class": "block w-full rounded-lg border-0 bg-gray-700 text-white px-3 py-2 shadow-sm ring-1 ring-inset ring-gray-600 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-500 sm:text-sm",
                "accept": ".pdf",
            }
        )
    )

    class Meta:
        model = ResumeAnalysis
        fields = ["resume_file", "job_title", "job_description"]

    def clean_resume_file(self):
        resume = self.cleaned_data["resume_file"]
        if not resume.name.lower().endswith(".pdf"):
            raise ValidationError("Only PDF files are allowed")
        return resume
