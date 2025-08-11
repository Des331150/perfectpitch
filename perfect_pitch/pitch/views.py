from django.views.generic import CreateView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser, ResumeAnalysis
from .services import process_resume
from .forms import UserRegistrationForm, UserLoginForm, ResumeAnalysisForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.shortcuts import redirect
from django.core.files.storage import default_storage
import os


# Create your views here.
class SignupView(CreateView):
    model = CustomUser
    form_class = UserRegistrationForm
    template_name = "signup.html"
    success_url = reverse_lazy("pitch:login")


class Login_view(LoginView):
    form_class = UserLoginForm  # Use form_class instead of authentication_form
    template_name = "login.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("pitch:homepage")

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        return super().form_valid(form)


class HomepageView(TemplateView):
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["form"] = ResumeAnalysisForm()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("pitch:login")

        form = ResumeAnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the file temporarily
            resume_file = form.cleaned_data["resume_file"]
            temp_path = default_storage.save(f"temp/{resume_file.name}", resume_file)

            try:
                # Process resume to get the score
                results = process_resume(
                    default_storage.path(temp_path),
                    form.cleaned_data["job_title"],
                    form.cleaned_data["job_description"],
                )

                # Create and save analysis with score
                analysis = form.save(commit=False)
                analysis.user = request.user
                analysis.score = results.get("overall_score", 0)
                analysis.save()

                # Store results in session
                request.session["analysis_results"] = results

                # Clean up temp file
                default_storage.delete(temp_path)

                return redirect("pitch:results")

            except Exception as e:
                # Clean up temp file on error
                default_storage.delete(temp_path)
                raise e

        # If form is invalid, show form with errors
        return self.render_to_response(self.get_context_data(form=form))


class ResultsView(LoginRequiredMixin, TemplateView):
    template_name = "results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["analysis_results"] = kwargs.get("analysis_results", {})
        return context
