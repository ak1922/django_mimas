from django.db import models

from .patients_model import Patient
from .patientinsurance_model import PatientInsurance
from .archivedappointment_model import ArchivedPatientAppointment
from .archivedvisit_model import ArchivedPatientVisit
from .auxiliary_models import DateTimeAuditModel
from mimascompany.models.employee_model import Employee
from mimascompany.models.dentist_model import Dentist
from mimascompany.models.branch_model import Branch


# Archived patient treatment
class ArchivedPatientTreatment(DateTimeAuditModel):

    treatment_title = models.CharField(max_length=300)
    teeth_number = models.CharField(null=True, blank=True)
    closed = models.BooleanField(default=True)

    notes = models.CharField(blank=True, null=True)
    medication = models.CharField(
        max_length=300,
        null=True, blank=True
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
    visit = models.ForeignKey(
        ArchivedPatientVisit,
        null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f'{self.treatment_title} - {self.patient.full_name}'

    class Meta(DateTimeAuditModel.Meta):
        ordering = ['created']
        verbose_name = 'Archived Patient Treatment'
        verbose_name_plural = 'Archived Patients Treatments'
