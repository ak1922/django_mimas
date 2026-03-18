from django.db import models
from django.db.models import Q

from mimascompany.models import Employee, Dentist, Branch
from patients.models import (
    Patient,
    PatientVisit,
    PatientInsurance,
    PatientAppointment,
    DateTimeAuditModel
)


# ---- Custom queryset ----
class DentistReportQureySet(models.QuerySet):

    def closed_reports(self):
        return self.filter(closed=True)

    def open_reports(self):
        return self.filter(closed=False)

    def dentist_with_reports(self):
        return self.filter(
            Q(dentistreport_dentist__in=self.open_reports())
        ).distinct()


# ---- Custom model manager ----
class DentistReportManager(models.Manager.from_queryset(DentistReportQureySet)):
    pass


# ---- Dentist report model ----
class DentistReport(DateTimeAuditModel):

    report_title = models.CharField(max_length=300)
    history = models.TextField(blank=True, null=True)
    clinical_finding = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    general_comments = models.TextField(blank=True, null=True)
    closed = models.BooleanField(default=False)

    # ---- Related models ----
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='dentistreport_patient'
    )
    dentist = models.ForeignKey(
        Dentist,
        null=True,
        on_delete=models.SET_NULL,
        related_name='dentistreport_dentist'
    )
    branch = models.ForeignKey(
        Branch,
        null=True,
        on_delete=models.SET_NULL,
        related_name='dentistreport_branch'
    )
    insurance = models.ForeignKey(
        PatientInsurance,
        null=True,
        on_delete=models.SET_NULL,
        related_name='dentistreport_insurance'
    )
    appointment = models.ForeignKey(
        PatientAppointment,
        null=True,
        on_delete=models.SET_NULL,
        related_name='dentistreport_appointment'
    )
    visit = models.ForeignKey(
        PatientVisit,
        on_delete=models.CASCADE,
        related_name='dentistreport_visit'
    )
    updated_by = models.ForeignKey(
        Employee,
        null=True,
        on_delete=models.SET_NULL,
        related_name='dentistreport_updatedby'
    )

    objects = models.Manager()
    reports = DentistReportManager()

    def __str__(self):
        return self.report_title

    class Meta(DateTimeAuditModel.Meta):
        db_table = 'dentist_report'
        ordering = ['-created']
        verbose_name = 'Dentist Report'
        verbose_name_plural = 'Dentists Reports'
        indexes = [
            models.Index(fields=['closed'], name='dr_closed_idx'),
            models.Index(fields=['dentist', 'closed'], name='dr_dentistclosed_idx'),
            models.Index(fields=['patient', 'closed'], name='dr_patientclosed_idx')
        ]
