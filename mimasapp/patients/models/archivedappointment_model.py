from django.db import models

from patients.models import PatientInsurance, Patient
from mimascompany.models import Branch, Dentist, Employee


# Archived appointment model
class ArchivedPatientAppointment(models.Model):

    confirmed = models.BooleanField(default=True)
    appointment_title = models.CharField(max_length=300)
    appointment_date = models.DateField()

    appointment_time = models.CharField(max_length=10)
    reason = models.TextField(max_length=600)
    status = models.CharField(max_length=20)


    archived = models.CharField(null=True, blank=True)
    updated = models.CharField(blank=True, null=True)


    patient = models.ForeignKey(
        Patient,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedappointment_patient'
    )
    dentist = models.ForeignKey(
        Dentist,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedappointment_dentist'
    )
    branch = models.ForeignKey(
        Branch,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedappointment_patient'
    )
    insurance = models.ForeignKey(
       PatientInsurance,
       null=True,
       on_delete=models.SET_NULL,
        related_name='archivedappointment_insurabce'
    )
    updated_by = models.ForeignKey(
        Employee,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedappointment_updatedby'
    )

    def __str__(self):
        return f'{self.appointment_title} for {self.patient}'

    class Meta:
        ordering =['archived']
        verbose_name = 'Archived Patient Appointment'
        verbose_name_plural = 'Archived Patients Appointments'
