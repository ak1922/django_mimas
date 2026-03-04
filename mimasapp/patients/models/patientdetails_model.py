from django.db import models
from django.utils.translation import gettext_lazy as _

from mimascompany.models.employee_model import Employee
from mimascompany.models.dentist_model import Dentist
from patients.models.patients_model import Patient
from patients.models.auxiliary_models import DateTimeAuditModel


# Patient details model
class PatientDetail(DateTimeAuditModel):

    class BlodType(models.TextChoices):
        TYPEA = 'Type A', _('Type A')
        TYPEAB = 'Type AB', _('Type AB')
        TYPEO = 'Type O', _('Type O')

    ssn = models.CharField(max_length=15)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    blood_type = models.CharField(choices=BlodType.choices)
    allergies = models.CharField(blank=True, null=True)
    height = models.DecimalField(
        blank=True, null=True,
        max_digits=5, decimal_places=2
    )
    weight = models.DecimalField(
        blank=True, null=True,
        max_digits=5, decimal_places=2
    )
    current_medication = models.CharField(
        max_length=300,
        blank=True, null=True
    )

    # ---- Related models ----
    patient = models.OneToOneField(
        Patient,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name='patientdetail_patient'
    )
    updated_by = models.ForeignKey(
        Employee,
        blank=True, null=True,
        on_delete=models.PROTECT,
        related_name='patientdetail_updatedby'
    )
    secondary_dentist = models.ManyToManyField(
        Dentist,
        related_name='patientdetail_secondarydentist'
    )

    def __str__(self):
        pass

    class Meta(DateTimeAuditModel.Meta):
        ordering = ['created']
        verbose_name = 'Patient Detail'
        verbose_name_plural = 'Patient Details'
