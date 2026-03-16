from django.db import models

from patients.models.archivedreferral_model import ArchivedPatientReferral
from patients.models.archivedlab_model import ArchivedPatientLab
from patients.models.archivedtreatment_model import ArchivedPatientTreatment
from patients.models.patientreferral_model import PatientReferral
from patients.models.patienttreatment_model import PatientTreatment
from patients.models.patientlab_model import PatientLab
from patients.models.patients_model import Patient
from mimascompany.models.dentist_model import Dentist


# Dentist message
class DentistOfficeMessage(models.Model):

    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    # ---- Related models ----
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        null=True
    )
    dentist = models.ForeignKey(
        Dentist,
        on_delete=models.CASCADE,
        null=True
    )
    lab = models.ForeignKey(
        PatientLab,
        on_delete=models.CASCADE,
        null=True
    )
    referral = models.ForeignKey(
        PatientReferral,
        on_delete=models.CASCADE,
        null=True
    )
    treatment = models.ForeignKey(
        PatientTreatment,
        on_delete=models.CASCADE,
        null=True
    )
    archived_lab = models.ForeignKey(
        ArchivedPatientLab,
        on_delete=models.CASCADE,
        null=True
    )
    archived_referral = models.ForeignKey(
        ArchivedPatientReferral,
        on_delete=models.CASCADE,
        null=True
    )
    archived_treatment = models.ForeignKey(
        ArchivedPatientTreatment,
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return self.patient

    class Meta:
        verbose_name = 'Dentist Office Message'
        verbose_name_plural = 'Dentist Office Messages'

