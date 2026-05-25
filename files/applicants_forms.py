from django import forms
from .models import Applicant, Resume, ApplicantPassport, ApplicantWorkBook


class NoClearFileInput(forms.FileInput):
    pass


class ApplicantProfileForm(forms.ModelForm):
    class Meta:
        model  = Applicant
        fields = [
            'last_name', 'first_name', 'middle_name',
            'date_of_birth', 'gender', 'phone', 'avatar',
            'country', 'city', 'address', 'about', 'status',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'about':         forms.Textarea(attrs={'rows': 4}),
            'avatar':        NoClearFileInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_of_birth'].input_formats = ['%Y-%m-%d']


class PassportForm(forms.ModelForm):
    class Meta:
        model  = ApplicantPassport
        fields = ['series', 'number', 'scan']
        widgets = {
            'series': forms.TextInput(attrs={'placeholder': '1234'}),
            'number': forms.TextInput(attrs={'placeholder': '567890'}),
            'scan':   NoClearFileInput(),
        }


class WorkBookForm(forms.ModelForm):
    class Meta:
        model  = ApplicantWorkBook
        fields = ['number', 'scan']
        widgets = {
            'number': forms.TextInput(attrs={'placeholder': 'АТ-III №1234567'}),
            'scan':   NoClearFileInput(),
        }


class ResumeForm(forms.ModelForm):
    class Meta:
        model  = Resume
        fields = [
            'title', 'experience_years', 'salary_expected',
            'education', 'skills', 'resume_pdf', 'status',
        ]
        widgets = {
            'skills':     forms.Textarea(attrs={'rows': 3, 'placeholder': 'Python, Django, PostgreSQL...'}),
            'resume_pdf': NoClearFileInput(),
        }
