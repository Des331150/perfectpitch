from django.contrib.auth.forms import forms, UserCreationForm, ValidationError
from .models import CustomUser
from django.contrib.auth import authenticate
import os


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["name", "email", "password1", "password2"]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")


class UserLoginForm(forms.Form):
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
