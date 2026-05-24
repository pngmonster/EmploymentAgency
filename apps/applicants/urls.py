from django.urls import path
from . import views

app_name = 'applicants'

urlpatterns = [
    path('profile/',              views.profile_view,       name='profile'),
    path('resumes/',              views.resume_list_view,   name='resume_list'),
    path('resumes/create/',       views.resume_create_view, name='resume_create'),
    path('resumes/<int:pk>/edit/',   views.resume_edit_view,   name='resume_edit'),
    path('resumes/<int:pk>/delete/', views.resume_delete_view, name='resume_delete'),
    path('applications/',         views.applications_view,  name='applications'),
]
