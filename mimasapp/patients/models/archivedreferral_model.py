from django.db import models

from .patientinsurance_model import PatientInsurance
from .patients_model import Patient
from .archivedvisit_model import ArchivedPatientVisit
from .archivedappointment_model import ArchivedPatientAppointment
from mimascompany.models.branch_model import Branch
from mimascompany.models.dentist_model import Dentist
from mimascompany.models.employee_model import Employee


# Archived referral
class ArchivedPatientReferral(models.Model):

    referral_title = models.CharField(max_length=300)
    referral_date = models.CharField()
    refer_phone = models.CharField(max_length=15)
    reason = models.CharField()
    extra_details = models.CharField()
    closed = models.BooleanField(default=True)

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
        pass

    class Meta:
        verbose_name = 'Archived Patient Referral'
        verbose_name_plural = 'Archived Patients Referrals'

