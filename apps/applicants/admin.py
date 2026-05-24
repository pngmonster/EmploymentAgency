from django.contrib import admin
from .models import Applicant, ApplicantPassport, ApplicantWorkBook, Resume


class PassportInline(admin.StackedInline):
    model = ApplicantPassport
    extra = 0

class WorkBookInline(admin.StackedInline):
    model = ApplicantWorkBook
    extra = 0

class ResumeInline(admin.TabularInline):
    model = Resume
    extra = 0
    fields = ('title', 'experience_years', 'salary_expected', 'status')

@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display  = ('get_full_name', 'user', 'city', 'status', 'created_at')
    list_filter   = ('status', 'gender', 'city')
    search_fields = ('last_name', 'first_name', 'user__email')
    inlines       = [PassportInline, WorkBookInline, ResumeInline]

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display  = ('title', 'applicant', 'experience_years', 'salary_expected', 'status')
    list_filter   = ('status', 'education')
    search_fields = ('title', 'applicant__last_name')
