from django.db import models

from mimascompany.models import PatientBooking
from patients.models import (
    Patient,
    PatientVisit,
    PatientBill,
    ArchivedPatientVisit,
    PatientAppointment,
    ArchivedPatientAppointment,
)


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
        'patients.ArchivedPatientBill',
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    def __str__(self):
        return self.message[:50]

    class Meta:
        db_table = 'patient_messages'
        ordering = ['-created']
        verbose_name = 'Patient Message'
        verbose_name_plural = 'Patients Messages'
