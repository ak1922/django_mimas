from django.contrib import admin

from patients.models import (
    Patient,
    PatientLab,
    PatientBill,
    PatientBooking,
    PatientVisit,
    PatientDetail,
    PatientContact,
    PatientMessage,
    TreatmentRoom,
    PatientReferral,
    PatientTreatment,
    PatientInsurance,
    PatientVisitTask,
    PatientAppointment,
    PostVisitOption,
    ArchivedPatientLab,
    ArchivedPatientBill,
    ArchivedPatientVisit,
    ArchivedPatientReferral,
    ArchivedPatientTreatment,
    ArchivedPatientAppointment
)


admin.site.register(PostVisitOption)
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
    ordering = ['created']
    list_per_page = 10
    search_fields = [
        'patient__last_name',
        'patient__first_name',
        'blood_type',
        'secondary_dentist__patients_primarydentist__first_name',
        'secondary_dentist__patients_primarydentist__last_name'
    ]



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


@admin.register(ArchivedPatientAppointment)
class ArchivedPatientAppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'dentist', 'branch', 'appointment_title', 'appointment_date', 'appointment_title', 'archived', 'updated_by']
    ordering = ['archived']
    search_fields = [
        'patient__last_name',
        'patient__first_name',
        'dentist__patients_primarydentist__last_name',
        'dentist__patients_primarydentist__first_name'
    ]


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


@admin.register(ArchivedPatientVisit)
class ArchivedPatientVisitAdmin(admin.ModelAdmin):
    list_display = ['patient', 'appointment', 'visit_title', 'dentist', 'branch', 'updated', 'updated_by']
    ordering = ['archived']
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


@admin.register(PatientBill)
class PatientBillAdmin(admin.ModelAdmin):
    list_display = ['patient', 'appointment', 'visit', 'bill_title', 'total_charge', 'is_paid', 'updated_by']
    ordering = ['created']
    search_fields = [
        'bill_title',
        'patient__last_name',
        'patient__first_name'
    ]

@admin.register(ArchivedPatientBill)
class ArchivedPatientBillAdmin(admin.ModelAdmin):
    list_display = ['patient', 'appointment', 'visit', 'bill_title', 'total_charge', 'is_paid', 'updated_by']
    search_fields = [
        'bill_title',
        'patient__last_name',
        'patient__first_name'
    ]


@admin.register(PatientLab)
class PatientLabAdmin(admin.ModelAdmin):
    list_display = ['patient', 'dentist', 'appointment', 'visit', 'insurance', 'lab_title', 'updated', 'updated_by']
    ordering = ['created']
    search_fields = [
        'lab_title',
        'appointment__patient__first_name',
        'appointment__patient__last_name',
        'dentist__employee__last_name',
        'dentist__employee__first_name'
    ]

@admin.register(ArchivedPatientLab)
class ArchivedPatientLabAdmin(admin.ModelAdmin):
    list_display = ['patient', 'dentist', 'appointment', 'visit', 'insurance', 'lab_title', 'archived', 'updated_by']
    ordering = ['archived']
    search_fields = [
        'lab_title',
        'appointment__patient__first_name',
        'appointment__patient__last_name',
        'dentist__employee__last_name',
        'dentist__employee__first_name'
    ]


@admin.register(PatientTreatment)
class PatientTreatmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'dentist', 'appointment', 'visit', 'insurance', 'treatment_title', 'updated', 'updated_by']
    ordering = ['created']
    search_fields = [
        'treatment_title',
        'appointment__patient__first_name'
    ]


@admin.register(ArchivedPatientTreatment)
class ArchivedPatientTreatmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'dentist', 'appointment', 'visit', 'insurance', 'treatment_title', 'archived', 'updated_by']
    ordering = ['archived']
    search_fields = ['treatment_title']


@admin.register(PatientReferral)
class PatientReferralAdmin(admin.ModelAdmin):
    list_display = ['patient', 'dentist', 'appointment', 'visit', 'insurance', 'referral_title', 'updated', 'updated_by']
    ordering = ['created']
    search_fields = ['referral_title']


@admin.register(ArchivedPatientReferral)
class ArchivedPatientReferralAdmin(admin.ModelAdmin):
    list_display = ['patient', 'dentist', 'appointment', 'visit', 'insurance', 'referral_title', 'updated', 'updated_by']
    ordering = ['archived']
    search_fields = ['referral_title']


@admin.register(TreatmentRoom)
class TreatmentRoomAdmin(admin.ModelAdmin):
    list_display = ['room_name', 'room_number', 'is_occupied', 'branch', 'created', 'updated', 'updated_by']
    ordering = ['room_name']
    search_fields = ['room_name', 'room_number']
