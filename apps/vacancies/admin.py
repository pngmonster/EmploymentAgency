from django.contrib import admin
from .models import Vacancy, Application

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display  = ('title', 'employer', 'city', 'work_format', 'status', 'created_at')
    list_filter   = ('status', 'work_format', 'employment_type')
    search_fields = ('title', 'employer__company_name')
    list_editable = ('status',)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display  = ('resume', 'vacancy', 'status', 'created_at')
    list_filter   = ('status',)
    search_fields = ('resume__applicant__last_name', 'vacancy__title')
