from django.urls import path

from .views.dentist_office import dentist_office
from .views.dentist_dashboard import dentist_dashboard


app_name = 'dentists'

urlpatterns = [
    path('dentistoffice/', dentist_office, name='dentistoffice'),
    path('dentistdashboard/', dentist_dashboard, name='dentistdashboard'),
]
