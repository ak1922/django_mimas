from django.db import models

from .patients_model import Patient
from .patientappointment_model import PatientBooking, PatientAppointment
from .patientvisit_models import PatientVisit
from .patientbill_model import PatientBill, ArchivedPatientBill
from .archivedvisit_model import ArchivedPatientVisit
from .archivedappointment_model import ArchivedPatientAppointment


# Patient center messages
class PatientMessage(models.Model):

    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    # ---- Related models ----
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    booking = models.ForeignKey(
        PatientBooking,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    appointment = models.ForeignKey(
        PatientAppointment,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    visit = models.ForeignKey(
        PatientVisit,
        null=True, blank=True,
        on_delete=models.CASCADE,
    )

    bill = models.ForeignKey(
        PatientBill,
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    archived_appointment = models.ForeignKey(
        ArchivedPatientAppointment,
        null=True, blank=True,
        on_delete=models.CASCADE
    )
    archived_visit = models.ForeignKey(
        ArchivedPatientVisit,
        null=True, blank=True,
        on_delete=models.CASCADE
    )
    archived_bill = models.ForeignKey(
        ArchivedPatientBill,
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    def __str__(self):
        return self.message[:50]

    class Meta:
        ordering = ['-created']
        verbose_name = 'Patient Message'
        verbose_name_plural = 'Patients Messages'
