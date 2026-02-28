from django.contrib import admin

from patients.models.patients_model import Patient
from patients.models.patientcontact_model import PatientContact


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):

    list_display = ['patient_username', 'first_name', 'last_name', 'gender', 'primary_dentist', 'created', 'updated', 'updated_by']
    search_fields = ['first_name', 'last_name', 'primary_dentist__employee__first_name', 'primary_dentist__employee__last_name']
    ordering = ['created']


@admin.register(PatientContact)
class PatientContactAdmin(admin.ModelAdmin):
    list_display = ['contact_name', 'patient', 'contact_phone', 'contact_address', 'created', 'updated', 'updated_by']
    search_fields = ['contact_name', 'patient__last_name', 'patient__first_name']
    ordering = ['created']
