from django.contrib.auth.forms import (
    forms,
    UserCreationForm,
    ValidationError,
    AuthenticationForm,
)
from .models import CustomUser
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


class UserLoginForm(AuthenticationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        def __init__(self, *args, **kwargs):
            self.request = kwargs.pop("request", None)
            super().__init__(*args, **kwargs)

        if email and password:
            self.user_cache = authenticate(email=email, password=password)

            if self.user_cache is None:
                raise forms.ValidationError("Invalid email or password.")

        return cleaned_data


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
