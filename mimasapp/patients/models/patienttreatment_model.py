from django.db import models
from django.db.models import Q

from mimascompany.models import Branch, Dentist, Employee
from patients.models import (
    Patient,
    PatientVisit,
    PatientInsurance,
    PatientAppointment,
    DateTimeAuditModel
)


# ----- Custom queryset
class PatientTreatmentQuerySet(models.QuerySet):

    def open_treatments(self):
        return self.filter(Q(closed=False))

    def closed_treatments(self):
        return self.filter(Q(closed=True))

    def with_related(self):
        return self.select_related('patient', 'dentist', 'visit', 'branch')


# ----- Custom manager
class PatientTreatmentManager(models.Manager.from_queryset(PatientTreatmentQuerySet)):
    pass


# Patient treatment model
class PatientTreatment(DateTimeAuditModel):

    treatment_title  = models.CharField(max_length=300)
    teeth_number = models.CharField(
        null=True, blank=True,
        max_length=5
    )
    closed = models.BooleanField(default=False)

    notes = models.TextField(null=True, blank=True)
    medication = models.CharField(
        max_length=300,
        blank=True, null=True
    )

    # ---- ForeignKeys ----
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='patienttreatment_patient'
    )
    dentist = models.ForeignKey(
        Dentist,
        null=True,
        on_delete=models.SET_NULL,
        related_name='patienttreatment_dentist'
    )
    branch = models.ForeignKey(
        Branch,
        null=True,
        on_delete=models.SET_NULL,
        related_name='patienttreatment_branch'
    )
    insurance = models.ForeignKey(
        PatientInsurance,
        null=True,
        on_delete=models.SET_NULL,
        related_name='patienttreatment_insurance'
    )
    appointment = models.ForeignKey(
        PatientAppointment,
        null=True,
        on_delete=models.SET_NULL,
        related_name='patienttreatment_appointment'
    )
    visit = models.ForeignKey(
        PatientVisit,
        on_delete=models.CASCADE,
        related_name='patienttreatment_visit'
    )
    updated_by = models.ForeignKey(
        Employee,
        null=True,
        on_delete=models.CASCADE,
        related_name='patienttreatment_updatedby'
    )

    # ------- Managers ---------
    objects = PatientTreatmentQuerySet.as_manager()

    @property
    def closed_visit(self):
        """ Return closed patient visit """
        if self.visit and self.visit.visit_status == 'Closed':
            return True
        return False

    @property
    def is_finalized(self):
        return self.closed or (self.visit and self.visit.visit_status == 'Closed')

    @property
    def needs_attention(self):
        return not self.is_finalized

    @property
    def closed_treatment(self):
        if self.closed:
            return True
        return False

    def __str__(self):
        return f'{self.treatment_title}'

    class Meta(DateTimeAuditModel.Meta):
        db_table = 'patient_treatments'
        ordering = ['created']
        verbose_name = 'Patient Treatment'
        verbose_name_plural = 'Patients Treatments'
        indexes = [
            models.Index(fields=['closed'], name='pt_closed_idx'),
            models.Index(fields=['patient', 'closed'], name='pt_patientclosed_idx'),
            models.Index(fields=['branch', 'closed'], name='pt_branchclosed_idx'),
            models.Index(fields=['dentist', 'closed'], name='pt_dentistclosed_idx'),
            models.Index(fields=['patient', '-created'], name='pt_patientcreated_idx')
        ]
