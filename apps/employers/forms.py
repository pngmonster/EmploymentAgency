from django import forms
from .models import Employer


class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model  = Employer
        fields = [
            'company_name', 'inn', 'industry', 'founded_year',
            'website', 'logo', 'about', 'phone',
            'contact_person', 'country', 'city', 'address',
        ]
        widgets = {
            'about': forms.Textarea(attrs={'rows': 4}),
        }
