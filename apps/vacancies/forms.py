from django import forms
from .models import Vacancy, Application


class VacancyForm(forms.ModelForm):
    class Meta:
        model  = Vacancy
        fields = [
            'title', 'about', 'experience_years',
            'salary_min', 'salary_max', 'employment_type',
            'schedule', 'work_format', 'country', 'city', 'address',
            'contact_name', 'contact_phone', 'contact_email',
            'status', 'expires_at',
        ]
        widgets = {
            'about':      forms.Textarea(attrs={'rows': 5}),
            'expires_at': forms.DateInput(attrs={'type': 'date'}),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model  = Application
        fields = ['resume', 'cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Кратко расскажите почему вы подходите на эту позицию...'
            }),
        }

    def __init__(self, *args, applicant=None, **kwargs):
        super().__init__(*args, **kwargs)
        if applicant:
            self.fields['resume'].queryset = applicant.resumes.filter(status='active')
            self.fields['resume'].label = 'Резюме'
