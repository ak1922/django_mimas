from django.db import models
from django.utils.translation import gettext_lazy as _

from patients.models.patients_model import Patient
from patients.models.auxiliary_models import DateTimeAuditModel
from mimascompany.models.employee_model import Employee


# Patients contact model
class PatientContact(DateTimeAuditModel):

    # ---- Contact info ----
    contact_name = models.CharField(max_length=100)
    contact_address = models.CharField(max_length=200)
    contact_phone = models.CharField(max_length=15)
    relationship = models.CharField(max_length=20)

    # ---- Other model fields ----
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

    class Meta:
        ordering = ['created']
        verbose_name = _('PatientContact')
        verbose_name_plural = _('PatientContacts')
