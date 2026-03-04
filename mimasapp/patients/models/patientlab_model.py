from django.db import models

from .auxiliary_models import DateTimeAuditModel
from .patients_model import Patient
from .patientvisit_models import PatientVisit
from .patientappointment_model import PatientAppointment
from .patientinsurance_model import PatientInsurance
from mimascompany.models.branch_model import Branch
from mimascompany.models.dentist_model import Dentist
from mimascompany.models.employee_model import Employee


# Patient lab model
class PatientLab(DateTimeAuditModel):

    # ---- Lab info ----
    lab_title = models.CharField(max_length=300)
    laboratory_name = models.CharField(max_length=200)
    laboratory_address = models.CharField(max_length=300)
    laboratory_phone = models.CharField(max_length=15)
    due_date = models.DateField(blank=True, null=True)
    instructions = models.TextField()
    closed = models.BooleanField(default=False)

    # ---- Related models ----
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='patientlab_patient'
    )
    dentist = models.ForeignKey(
        Dentist,
        null=True,
        on_delete=models.SET_NULL,
        related_name='patientlab_dentist'
    )
    branch = models.ForeignKey(
        Branch,
        null=True,
        on_delete=models.SET_NULL,
        related_name='patientlab_branch'
    )
    insurance = models.ForeignKey(
        PatientInsurance,
        null=True,
        on_delete=models.SET_NULL,
        related_name='patientlab_insurance'
    )
    appointment = models.ForeignKey(
        PatientAppointment,
        null=True,
        on_delete=models.SET_NULL,
        related_name='patientlab_appointment'
    )
    visit = models.ForeignKey(
        PatientVisit,
        on_delete=models.CASCADE,
        related_name='patientlab_visit'
    )
    updated_by = models.ForeignKey(
        Employee,
        null=True,
        on_delete=models.SET_NULL,
        related_name='patientlab_updatedby'
    )

    def __str__(self):
        return self.lab_title

    class Meta(DateTimeAuditModel.Meta):
        ordering = ['created']
        verbose_name = 'Patient Lab'
        verbose_name_plural = 'Patient Labs'
