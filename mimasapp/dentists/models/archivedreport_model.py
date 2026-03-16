from django.db import models

from mimascompany.models import Employee, Dentist, Branch
from patients.models import Patient, PatientInsurance, ArchivedPatientVisit, ArchivedPatientAppointment


# Archived report
class ArchivedDentistReport(models.Model):

    archived_title = models.CharField(max_length=300)
    history = models.TextField(null=True, blank=True)
    clinical_finding = models.TextField(null=True, blank=True)
    diagnosis = models.TextField(null=True, blank=True)
    general_comments = models.TextField(null=True, blank=True)
    closed = models.BooleanField(default=True)

    # ---- Audit fields ----
    archived = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(blank=True, null=True)

    # ---- ForeignKeys ----
    patient = models.ForeignKey(
        Patient,
        on_delete=models.SET_NULL,
        null=True,
        related_name='archivedreport_patient'
    )
    dentist = models.ForeignKey(
        Dentist,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedreport_dentist'
    )
    branch = models.ForeignKey(
        Branch,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedreport_branch'
    )
    insurance = models.ForeignKey(
        PatientInsurance,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedreport_insurance'
    )
    appointment = models.ForeignKey(
        ArchivedPatientAppointment,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedreport_appointment'
    )
    visit = models.ForeignKey(
        ArchivedPatientVisit,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedreport_visit'
    )
    updated_by = models.ForeignKey(
        Employee,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedreport_updatedby'
    )

    def __str__(self):
        return self.archived_title

    class Meta:
        verbose_name = 'Archived Dentist Report'
        verbose_name_plural = 'Archived Dentists Reports'
