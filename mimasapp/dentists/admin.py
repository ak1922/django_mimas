from django.contrib import admin

from .models.dentistreport_model import DentistReport
from .models.auxiliary_models import DentistOfficeMessage
from .models.archivedreport_model import ArchivedDentistReport


# Dentist app models
admin.site.register(DentistOfficeMessage)


@admin.register(DentistReport)
class DentistReportAdmin(admin.ModelAdmin):
    list_display = [
        'patient',
        'dentist',
        'branch',
        'appointment',
        'visit',
        'closed',
        'created',
        'updated'
    ]
    search_fields = [
        'report_title',
        'patient__last_name',
        'patient__first_name',
        'dentist__employee__last_name',
        'dentist__employee__first_name',
    ]
    ordering = ['created']


@admin.register(ArchivedDentistReport)
class ArchivedDentistReportAdmin(admin.ModelAdmin):
    list_display = ['patient', 'dentist', 'branch', 'appointment', 'visit', 'archived_title', 'archived', 'updated_by']
    search_fields = [
        'archived_title',
        'patient__last_name',
        'patient__first_name',
        'dentist__employee__last_name',
        'dentist__employee__first_name',
    ]
    ordering = ['archived']
