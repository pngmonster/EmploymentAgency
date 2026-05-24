from django.urls import path
from . import views

app_name = 'vacancies'

urlpatterns = [
    path('',                            views.vacancy_list_view,         name='list'),
    path('<int:pk>/',                   views.vacancy_detail_view,       name='detail'),
    path('my/',                         views.vacancy_my_list_view,      name='my_list'),
    path('create/',                     views.vacancy_create_view,       name='create'),
    path('<int:pk>/edit/',              views.vacancy_edit_view,         name='edit'),
    path('<int:pk>/applications/',      views.vacancy_applications_view, name='applications'),
    path('application/<int:pk>/status/', views.application_status_view, name='application_status'),
]
