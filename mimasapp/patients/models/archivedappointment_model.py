from django.db import models

from mimascompany.models.employee_model import Employee
from mimascompany.models.branch_model import Branch
from mimascompany.models.dentist_model import Dentist
from patients.models.patients_model import Patient
from patients.models.patientinsurance_model import PatientInsurance


# Archived appointment model
class ArchivedPatientAppointment(models.Model):

    appointment_title = models.CharField(max_length=300)
    appointment_date = models.CharField()
    appointment_time = models.CharField()
    reason = models.TextField()
    status = models.CharField()

    archived = models.CharField(null=True, blank=True)
    updated = models.CharField(blank=True, null=True)
    updated_by = models.ForeignKey(
        Employee,
        null=True,
        on_delete=models.SET_NULL,
    )

    patient = models.ForeignKey(
       Patient,
       null=True,
       on_delete=models.SET_NULL
    )
    dentist = models.ForeignKey(
       Dentist,
       null=True,
       on_delete=models.SET_NULL
    )
    branch = models.ForeignKey(
       Branch,
       null=True,
       on_delete=models.SET_NULL
    )
    insurance = models.ForeignKey(
       PatientInsurance,
       null=True,
       on_delete=models.SET_NULL
    )

    def __str__(self):
        return f'{self.appointment_title} for {self.patient}'

    class Meta:
        ordering =['archived']
        verbose_name = 'Archived Patient Appointment'
        verbose_name_plural = 'Archived Patients Appointments'
