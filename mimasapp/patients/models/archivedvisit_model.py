from django.db import models

from .patients_model import Patient
from .patientinsurance_model import PatientInsurance
from .archivedappointment_model import ArchivedPatientAppointment
from mimascompany.models.employee_model import Employee
from mimascompany.models.dentist_model import Dentist
from mimascompany.models.branch_model import Branch


# Archived visit
class ArchivedPatientVisit(models.Model):

    visit_title = models.CharField(
        unique=True,
        max_length=300
    )
    visit_date = models.CharField(null=True, blank=True)
    visit_time = models.CharField(blank=True, null=True)
    visit_status = models.CharField(max_length=50)

    services = models.CharField(blank=True, null=True)
    departments = models.CharField(blank=True, null=True)
    visit_options = models.CharField(blank=True, null=True)
    total_price_aggregated = models.DecimalField(
        blank=True, null=True,
        max_digits=10, decimal_places=2
    )

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

    def __str__(self):
        return self.visit_title

    class Meta:
        verbose_name = 'Archived Patient Visit'
        verbose_name_plural = 'Archived Patients Visits'
