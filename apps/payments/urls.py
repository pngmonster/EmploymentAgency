from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('',        views.unpaid_list_view, name='unpaid_list'),
    path('pay-all/', views.pay_all_view,   name='pay_all'),
]
