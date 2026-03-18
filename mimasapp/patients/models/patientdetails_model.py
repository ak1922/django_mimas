from django.db import models

from mimascompany.models import Dentist, Employee
from patients.models import Patient, DateTimeAuditModel


# Patient details model
class PatientDetail(DateTimeAuditModel):

    class BlodType(models.TextChoices):
        TYPEA = 'Type A', 'Type A',
        TYPEAB = 'Type AB', 'Type AB',
        TYPEO = 'Type O', 'Type O'

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
        return f'{self.patient.full_name}'

    class Meta(DateTimeAuditModel.Meta):
        db_table = 'patient_details'
        ordering = ['created']
        verbose_name = 'Patient Detail'
        verbose_name_plural = 'Patient Details'
        indexes = [
            models.Index(fields=['patient', 'blood_type'], name='pd_patientbloodtype_idx'),
            models.Index(fields=['blood_type'], name='pd_bloodtype_idx'),
        ]
