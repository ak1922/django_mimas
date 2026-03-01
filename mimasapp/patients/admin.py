from django.contrib import admin

from patients.models.patients_model import Patient
from patients.models.patientcontact_model import PatientContact
from patients.models.patientdetails_model import PatientDetail
from patients.models.patientinsurance_model import PatientInsurance


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):

    list_display = ['patient_username', 'first_name', 'last_name', 'gender', 'primary_dentist', 'created', 'updated', 'updated_by']
    search_fields = [
        'first_name',
        'last_name',
        'primary_dentist__employee__first_name',
        'primary_dentist__employee__last_name'
    ]
    ordering = ['created']


@admin.register(PatientContact)
class PatientContactAdmin(admin.ModelAdmin):
    list_display = ['contact_name', 'patient', 'contact_phone', 'contact_address', 'created', 'updated', 'updated_by']
    search_fields = ['contact_name', 'patient__last_name', 'patient__first_name']
    ordering = ['created']


# Patient details admin
@admin.register(PatientDetail)
class PatientDetailAdmin(admin.ModelAdmin):
    list_display = ['patient', 'ssn', 'date_of_birth', 'phone_number', 'address', 'created', 'updated', 'updated_by']
    search_fields = [
        'patient__last_name',
        'patient__first_name',
        'blood_type',
        'secondary_dentist__patients_primarydentist__first_name',
        'secondary_dentist__patients_primarydentist__last_name'
    ]
    ordering = ['created']
    list_per_page = 10


# Patient insurance admin
@admin.register(PatientInsurance)
class PatientInsuranceAdmin(admin.ModelAdmin):
    list_display = ['patient', 'company', 'company_phone', 'policy_number', 'group_number', 'group_name', 'created', 'updated', 'updated_by']
    search_fields = ['patient__last_name', 'patient__first_name', 'company']
    ordering = ['created']
    list_per_page = 10
