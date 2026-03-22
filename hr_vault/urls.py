# hr_vault/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('add/', views.add_employee, name='add_employee'),
    path('employee/<int:employee_id>/', views.employee_detail, name='employee_detail'),
    path('employee/<int:employee_id>/delete/', views.delete_employee, name='delete_employee'),
    path('employee/<int:employee_id>/edit/', views.edit_employee, name='edit_employee'),
]
