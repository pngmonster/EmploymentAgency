from django import forms
from .models import Applicant, Resume


class ApplicantProfileForm(forms.ModelForm):
    class Meta:
        model  = Applicant
        fields = [
            'last_name', 'first_name', 'middle_name',
            'date_of_birth', 'gender', 'phone', 'avatar',
            'country', 'city', 'address', 'about', 'status',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'about':         forms.Textarea(attrs={'rows': 4}),
        }


class ResumeForm(forms.ModelForm):
    class Meta:
        model  = Resume
        fields = [
            'title', 'experience_years', 'salary_expected',
            'education', 'skills', 'resume_pdf', 'status',
        ]
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Python, Django, PostgreSQL...'}),
        }
