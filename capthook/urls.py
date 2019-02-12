from django.urls import path

from . import views

app_name = 'capthook'

urlpatterns = [
    path('all/', views.all_employees, name='all'),
    path('add/', views.add_employee, name='add'),
    path('<int:employee_id>/update/', views.update_employee, name='update'),
    path('<int:employee_id>/delete/', views.delete_employee, name='delete'),
]