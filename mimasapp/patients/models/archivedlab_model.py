from django.db import models

from mimascompany.models import Employee, Dentist, Branch
from patients.models import Patient, PatientInsurance, ArchivedPatientVisit, ArchivedPatientAppointment


# Archived lab
class ArchivedPatientLab(models.Model):

    closed = models.BooleanField(default=True)
    archived_title = models.CharField(max_length=300)
    laboratory_name = models.CharField(
        max_length=200,
        blank=True, null=True
    )
    laboratory_address = models.CharField(
        max_length=300,
        blank=True, null=True
    )
    laboratory_phone = models.CharField(
        max_length=15,
        blank=True, null=True
    )

    due_date = models.DateField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)

    archived = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(blank=True, null=True)

    # ---- ForeignKeys ----
    patient = models.ForeignKey(
        Patient,
        on_delete=models.SET_NULL,
        null=True,
        related_name='archivedlab_patient'
    )
    dentist = models.ForeignKey(
        Dentist,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedlab_dentist'
    )
    branch = models.ForeignKey(
        Branch,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedlab_branch'
    )
    insurance = models.ForeignKey(
        PatientInsurance,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedlab_insurance'
    )
    appointment = models.ForeignKey(
        ArchivedPatientAppointment,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedlab_appointment'
    )
    visit = models.ForeignKey(
        ArchivedPatientVisit,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedlab_visit'
    )
    updated_by = models.ForeignKey(
        Employee,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedlab_updatedby'
    )

    def __str__(self):
        return f'{self.patient} - {self.archived_title}'

    class Meta:
        db_table = 'archived_patient_labs'
        ordering = ['-archived']
        verbose_name = 'Archived Patient Lab'
        verbose_name_plural = 'Archived Patients Labs'
        indexes = [
            models.Index(fields=['archived'], name='apl_archived_idx'),
            models.Index(fields=['patient', 'closed'], name='apl_patientclosed_idx'),
            models.Index(fields=['dentist', 'closed'], name='apl_dentistclosed_idx'),
            models.Index(fields=['archived_title', 'updated_by'], name='archivedtitleupadtedby_idx'),
        ]
