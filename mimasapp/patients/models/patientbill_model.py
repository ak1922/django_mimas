from django.db import models

from mimascompany.models import Employee
from patients.models import (
    Patient,
    PatientVisit,
    PatientAppointment,
    DateTimeAuditModel
)


# Patient bill model
class PatientBill(DateTimeAuditModel):

    bill_title = models.CharField(
        max_length=300,
        unique=True
    )
    is_paid = models.BooleanField(default=False)
    total_charge = models.DecimalField(
        default=0.00,
        max_digits=10,
        decimal_places=2
    )

    # ---- Related models ----
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='patientbill_patient'
    )
    appointment = models.OneToOneField(
        PatientAppointment,
        on_delete=models.CASCADE,
        related_name='patientbill_appointment'
    )
    visit = models.OneToOneField(
        PatientVisit,
        on_delete=models.CASCADE,
        related_name='patientbill_visit'
    )
    updated_by = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='patientbill_updatedby'
    )

    def calculate_total_charge(self):
        """ Method to calculate total charge based on related services """
        if self.visit:
            return sum(service.price for service in self.visit.services.all())
        return 0.00

    @property
    def totalcharge(self):
        self.total_charge = self.calculate_total_charge()
        return self.total_charge

    def __str__(self):
        return f'{self.bill_title}'

    class Meta(DateTimeAuditModel.Meta):
        verbose_name = 'Patient Bill'
        db_table = 'patient_bills'
        verbose_name_plural = 'Patient Bills'
        indexes = [
            models.Index(fields=['is_paid'], name='pb_ispaid_idx'),
            models.Index(fields=['is_paid', 'total_charge'], name='pb_ispaidtotalcharge_idx'),
            models.Index(fields=['patient', 'visit'], name='pb_patientvisit_idx'),
            models.Index(fields=['patient', 'is_paid'], name='pb_patientispaid_idx')
        ]
