from django.db import models

from mimascompany.models import Employee
from patients.models import Patient, DateTimeAuditModel

# Patients contact model
class PatientContact(DateTimeAuditModel):

    # ---- Contact info ----
    contact_name = models.CharField(max_length=100)
    contact_address = models.CharField(max_length=200)
    contact_phone = models.CharField(max_length=15)
    relationship = models.CharField(max_length=20)

    # ---- Related models ----
    patient = models.OneToOneField(
        Patient,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='patientcontact_patient'
    )
    updated_by = models.ForeignKey(
        Employee,
        null=True, blank=True,
        on_delete=models.PROTECT,
        related_name='patientcontact_updatedby'
    )

    def __str__(self):
        return self.patient.full_name

    class Meta(DateTimeAuditModel.Meta):
        ordering = ['created']
        db_table = 'patient_contacts'
        verbose_name = 'Patient Contact'
        verbose_name_plural = 'Patient Contacts'
        indexes = [
            models.Index(fields=['patient', 'updated_by'], name='pc_patientupdatedby_idx')
        ]
