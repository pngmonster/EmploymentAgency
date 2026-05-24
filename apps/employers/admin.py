from django.contrib import admin
from .models import Employer

@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display  = ('company_name', 'industry', 'city', 'is_verified', 'created_at')
    list_filter   = ('is_verified', 'city')
    search_fields = ('company_name', 'inn', 'user__email')
    list_editable = ('is_verified',)
