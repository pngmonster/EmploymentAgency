from django.urls import path
from . import views

app_name = 'employers'

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('stats/',   views.stats_view,   name='stats'),
]
