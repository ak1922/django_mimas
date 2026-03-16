from django.db import models

from mimascompany.models import Branch, Dentist, Employee
from patients.models import Patient, PatientInsurance, ArchivedPatientVisit, ArchivedPatientAppointment


# Archived patient treatment
class ArchivedPatientTreatment(models.Model):

    closed = models.BooleanField(default=True)
    treatment_title = models.CharField(max_length=300)

    notes = models.CharField(
        blank=True, null=True,
        max_length=800
    )
    teeth_number = models.CharField(
        null=True, blank=True,
        max_length=5
    )
    medication = models.CharField(
        max_length=300,
        null=True, blank=True
    )

    archived = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(blank=True, null=True)

    # ---- ForeignKeys ----
    patient = models.ForeignKey(
        Patient,
        on_delete=models.SET_NULL,
        null=True,
        related_name='archivedtreatment_patient'
    )
    dentist = models.ForeignKey(
        Dentist,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedtreatment_dentist'
    )
    branch = models.ForeignKey(
        Branch,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedtreatment_branch'
    )
    insurance = models.ForeignKey(
        PatientInsurance,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedtreatment_insurance'
    )
    appointment = models.ForeignKey(
        ArchivedPatientAppointment,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedtreatment_appointment'
    )
    visit = models.ForeignKey(
        ArchivedPatientVisit,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedtreatment_visit',
    )
    updated_by = models.ForeignKey(
        Employee,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedtreatment_updatedby'
    )

    def __str__(self):
        return f'{self.treatment_title} - {self.patient.full_name}'

    class Meta:
        ordering = ['archived']
        verbose_name = 'Archived Patient Treatment'
        verbose_name_plural = 'Archived Patients Treatments'
