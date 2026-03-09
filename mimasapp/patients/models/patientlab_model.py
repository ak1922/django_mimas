from django.db import models

from .auxiliary_models import DateTimeAuditModel
from .patients_model import Patient
from .patientvisit_models import PatientVisit
from .patientappointment_model import PatientAppointment
from .patientinsurance_model import PatientInsurance
from mimascompany.models.branch_model import Branch
from mimascompany.models.dentist_model import Dentist
from mimascompany.models.employee_model import Employee


# --------- Custom queryset -----------
class PatientLabQuerySet(models.QuerySet):

    def open_labs(self):
        return self.filter(closed=False)

    def closed_labs(self):
        return self.filter(closed=True)

    def with_related(self):
        return self.select_related('patient', 'dentist')


# --------- Custom manager -----------
class PatientLabManager(models.Manager):
    def get_queryset(self):
        return PatientLabQuerySet(self.model, using=self._db)

    def open_labs(self):
        return self.get_queryset().open_labs()

    def closed_labs(self):
        return self.get_queryset().closed_labs()


# Patient lab model
class PatientLab(DateTimeAuditModel):

    # ---- Lab info ----
    lab_title = models.CharField(max_length=300)
    laboratory_name = models.CharField(max_length=200)
    laboratory_address = models.CharField(max_length=300)
    laboratory_phone = models.CharField(max_length=15)
    due_date = models.DateField(blank=True, null=True)
    instructions = models.TextField()
    closed = models.BooleanField(default=False)

    # ---- Related models ----
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='patientlab_patient'
    )
    dentist = models.ForeignKey(
        Dentist,
        null=True,
        on_delete=models.SET_NULL,
        related_name='patientlab_dentist'
    )
    branch = models.ForeignKey(
        Branch,
        null=True,
        on_delete=models.SET_NULL,
        related_name='patientlab_branch'
    )
    insurance = models.ForeignKey(
        PatientInsurance,
        null=True,
        on_delete=models.SET_NULL,
        related_name='patientlab_insurance'
    )
    appointment = models.ForeignKey(
        PatientAppointment,
        null=True,
        on_delete=models.SET_NULL,
        related_name='patientlab_appointment'
    )
    visit = models.ForeignKey(
        PatientVisit,
        on_delete=models.CASCADE,
        related_name='patientlab_visit'
    )
    updated_by = models.ForeignKey(
        Employee,
        null=True,
        on_delete=models.SET_NULL,
        related_name='patientlab_updatedby'
    )

    # ---- Managers ----
    objects = models.Manager()
    all_patientlabs = PatientLabManager()

    @property
    def closed_visit(self):
        """ Return closed patient visit """
        if self.visit and self.visit.visit_status == 'Closed':
            return True
        return False


    def __str__(self):
        return self.lab_title

    class Meta(DateTimeAuditModel.Meta):
        ordering = ['created']
        verbose_name = 'Patient Lab'
        verbose_name_plural = 'Patient Labs'
