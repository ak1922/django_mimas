from django.db import models

from .patients_model import Patient
from .patientinsurance_model import PatientInsurance
from .patientappointment_model import PatientAppointment
from .patientvisit_models import PatientVisit
from .auxiliary_models import DateTimeAuditModel
from mimascompany.models.branch_model import Branch
from mimascompany.models.dentist_model import Dentist
from mimascompany.models.employee_model import Employee


# Patient treatment model
class PatientTreatment(DateTimeAuditModel):

    treatment_title  = models.CharField(max_length=300)
    teeth_number = models.CharField(null=True, blank=True)
    closed = models.BooleanField(default=False)

    notes = models.TextField()
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
        ordering = ['created']
        verbose_name = 'Patient Treatment'
        verbose_name_plural = 'Patients Treatments'
