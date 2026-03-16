from django.db import models

from mimascompany.models import Employee, Dentist, Branch
from patients.models import Patient, PatientInsurance, ArchivedPatientVisit, ArchivedPatientAppointment


# Archived referral
class ArchivedPatientReferral(models.Model):

    closed = models.BooleanField(default=True)
    referral_title = models.CharField(max_length=300)
    referral_date = models.DateField(blank=True, null=True)

    refer_phone = models.CharField(
        max_length=15,
        blank=True, null=True
    )
    reason = models.CharField(
        max_length=800,
        null=True, blank=True
    )
    extra_details = models.CharField(
        max_length=800,
        blank=True, null=True
    )

    archived = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(blank=True, null=True)

    # ---- ForeignKeys ----
    patient = models.ForeignKey(
        Patient,
        on_delete=models.SET_NULL,
        null=True,
        related_name='archivedpatientreferral_patient'
    )
    dentist = models.ForeignKey(
        Dentist,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedpatientreferral_dentist'
    )
    branch = models.ForeignKey(
        Branch,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedpatientreferral_branch'
    )
    insurance = models.ForeignKey(
        PatientInsurance,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedpatientreferral_insurance'
    )
    appointment = models.ForeignKey(
        ArchivedPatientAppointment,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedpatientreferral_appointment'
    )
    visit = models.ForeignKey(
        ArchivedPatientVisit,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedpatientreferral_visit'
    )
    updated_by = models.ForeignKey(
        Employee,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedpatientreferral_updated_by'
    )

    def __str__(self):
        return f'{self.referral_title} - {self.patient}'

    class Meta:
        db_table = 'archived_patient_referrals'
        verbose_name = 'Archived Patient Referral'
        verbose_name_plural = 'Archived Patients Referrals'
