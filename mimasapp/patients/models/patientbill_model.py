from django.db import models

from mimascompany.models.employee_model import Employee
from patients.models.patients_model import Patient
from patients.models.auxiliary_models import DateTimeAuditModel
from patients.models.patientvisit_models import PatientVisit
from patients.models.patientappointment_model import PatientAppointment
from .archivedvisit_model import ArchivedPatientVisit
from .archivedappointment_model import ArchivedPatientAppointment


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
        verbose_name_plural = 'Patient Bills'


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
        verbose_name = 'Archived Patient Bill'
        verbose_name_plural = 'Archived Patients Bills'
