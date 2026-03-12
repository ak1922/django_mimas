from django.db import models

from mimascompany.models.branch_model import Branch
from mimascompany.models.dentist_model import Dentist
from mimascompany.models.employee_model import Employee
from patients.models.patients_model import Patient
from patients.models.archivedvisit_model import ArchivedPatientVisit
from patients.models.patientinsurance_model import PatientInsurance
from patients.models.archivedappointment_model import ArchivedPatientAppointment


# Archived report
class ArchivedDentistReport(models.Model):

    archived_title = models.CharField(max_length=300)
    history = models.TextField(null=True, blank=True)
    clinical_finding = models.TextField(null=True, blank=True)
    diagnosis = models.TextField(null=True, blank=True)
    general_comments = models.TextField(null=True, blank=True)
    closed = models.BooleanField(default=True)

    # ---- Audit fields ----
    archived = models.CharField(null=True, blank=True)
    updated = models.CharField(blank=True, null=True)
    updated_by = models.ForeignKey(
        Employee,
        null=True,
        on_delete=models.SET_NULL,
    )

    # ---- ForeignKeys ----
    patient = models.ForeignKey(
        Patient,
        on_delete=models.SET_NULL,
        null=True
    )
    dentist = models.ForeignKey(
        Dentist,
        null=True,
        on_delete=models.SET_NULL,
    )
    branch = models.ForeignKey(
        Branch,
        null=True,
        on_delete=models.SET_NULL,
    )
    insurance = models.ForeignKey(
        PatientInsurance,
        null=True,
        on_delete=models.SET_NULL,
    )
    appointment = models.ForeignKey(
        ArchivedPatientAppointment,
        null=True,
        on_delete=models.SET_NULL
    )
    visit = models.ForeignKey(
        ArchivedPatientVisit,
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.archived_title

    class Meta:
        verbose_name = 'Archived Dentist Report'
        verbose_name_plural = 'Archived Dentists Reports'
