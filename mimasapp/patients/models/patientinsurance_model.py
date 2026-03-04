from django.db import models

from patients.models.auxiliary_models import DateTimeAuditModel
from patients.models.patients_model import Patient
from mimascompany.models.employee_model import Employee


# Patient insurance model
class PatientInsurance(DateTimeAuditModel):

    # -----------------------
    company = models.CharField(max_length=80)
    policy_number = models.CharField(max_length=80)
    group_name = models.CharField(max_length=80)
    group_number = models.CharField(max_length=80)
    company_phone = models.CharField(max_length=14)
    subscriber_name = models.CharField(max_length=80)
    subscriber_dob = models.DateField()
    subscriber_relation_patient = models.CharField(max_length=20)

    # ---- Related models ----
    patient = models.OneToOneField(
        Patient,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name='patientinsurance_patient'
    )
    updated_by = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='patientinsurance_updatedby'
    )

    def __str__(self):
        return self.patient.full_name

    class Meta(DateTimeAuditModel.Meta):
        ordering = ['created']
        verbose_name = 'Patient Insurance'
        verbose_name_plural = 'Patients Insurance'
