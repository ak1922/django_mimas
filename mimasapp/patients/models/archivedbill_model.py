from django.db import models

from mimascompany.models import Employee
from patients.models import Patient , ArchivedPatientVisit, ArchivedPatientAppointment


# Archived patient bill
class ArchivedPatientBill(models.Model):

    bill_title = models.CharField(max_length=300)
    is_paid = models.BooleanField(default=True)

    total_charge = models.DecimalField(
        default=0.00,
        max_digits=10,
        decimal_places=2
    )

    archived = models.DateTimeField()
    updated = models.DateTimeField()

    patient = models.ForeignKey(
        Patient,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedbill_patient'
    )
    appointment = models.ForeignKey(
        ArchivedPatientAppointment,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedbill_appointment'
    )
    visit = models.ForeignKey(
        ArchivedPatientVisit,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedbill_visit'
    )
    updated_by = models.ForeignKey(
        Employee,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedbill_updatedby'
    )

    def __str__(self):
        return self.bill_title

    class Meta:
        db_table = 'archived_patient_bills'
        verbose_name = 'Archived Patient Bill'
        verbose_name_plural = 'Archived Patients Bills'
        indexes = [
            models.Index(fields=['patient', 'visit'], name='apb_patientvisit_idx'),
            models.Index(fields=['archived'], name='apb_archived_idx')
        ]
