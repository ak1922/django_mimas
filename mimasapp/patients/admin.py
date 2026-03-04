from django.contrib import admin

from patients.models.patients_model import Patient
from patients.models.patientcontact_model import PatientContact
from patients.models.patientdetails_model import PatientDetail
from patients.models.patientinsurance_model import PatientInsurance
from patients.models.patientappointment_model import PatientAppointment, PatientBooking
from patients.models.patientvisit_models import PatientVisit, PatientVisitTask, PostVisitOption
from patients.models.patientbill_model import PatientBill, ArchivedPatientBill
from patients.models.archivedvisit_model import ArchivedPatientVisit
from patients.models.archivedappointment_model import ArchivedPatientAppointment
from patients.models.patientlab_model import PatientLab
from patients.models.archivedlab_model import ArchivedPatientLab
from patients.models.patienttreatment_model import PatientTreatment
from patients.models.arcivedtreatment_model import ArchivedPatientTreatment
from patients.models.patientreferral_model import PatientReferral
from patients.models.archivedreferral_model import ArchivedPatientReferral
from patients.models.patientmessage_model import PatientMessage


admin.site.register(PostVisitOption)
admin.site.register(PatientBill)
admin.site.register(ArchivedPatientBill)
admin.site.register(ArchivedPatientVisit)
admin.site.register(ArchivedPatientAppointment)
admin.site.register(PatientLab)
admin.site.register(ArchivedPatientLab)
admin.site.register(PatientTreatment)
admin.site.register(ArchivedPatientTreatment)
admin.site.register(PatientReferral)
admin.site.register(ArchivedPatientReferral)
admin.site.register(PatientMessage)


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


# Patient appointment admin
@admin.register(PatientAppointment)
class PatientAppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'dentist', 'branch', 'appointment_title', 'appointment_date', 'appointment_title', 'created', 'updated', 'updated_by']
    search_fields = [
        'patient__last_name',
        'patient__first_name',
        'dentist__patients_primarydentist__last_name',
        'dentist__patients_primarydentist__first_name'
    ]
    ordering = ['-appointment_date', '-appointment_time']


# Patient visit admin
@admin.register(PatientVisit)
class PatientVisitAdmin(admin.ModelAdmin):
    list_display = ['patient', 'appointment', 'visit_title', 'dentist', 'branch', 'created', 'updated', 'updated_by']
    search_fields = [
        'patient__last_name',
        'patient__first_name',
        'dentist__patients_primarydentist__last_name',
        'dentist__patients_primarydentist__first_name',
        'branch__branch_name',
        'appointment__appointment_title'
    ]


@admin.register(PatientVisitTask)
class PatientVisitTaskAdmin(admin.ModelAdmin):
    list_display = ['assigned_to', 'task_title', 'visit', 'task_status', 'priority', 'created', 'updated']
    search_fields = ['assigned_to__user__first_name', 'assigned_to__user__last_name']


@admin.register(PatientBooking)
class PatientBookingAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'message', 'created', 'updated']
    search_fields = ['first_name', 'last_name', 'email']
