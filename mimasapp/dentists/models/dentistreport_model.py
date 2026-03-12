from django.db import models
from django.db.models import Q

from mimascompany.models.branch_model import Branch
from mimascompany.models.dentist_model import Dentist
from mimascompany.models.employee_model import Employee
from patients.models.patients_model import Patient
from patients.models.patientvisit_models import PatientVisit
from patients.models.auxiliary_models import DateTimeAuditModel
from patients.models.patientinsurance_model import PatientInsurance
from patients.models.patientappointment_model import PatientAppointment


class DentistReportQureySet(models.QuerySet):

    def closed_reports(self):
        return self.filter(closed=False)

    def open_reports(self):
        return self.filter(closed=True)

    def dentist_with_reports(self):
        return self.filter(
            Q(dentistreport_dentist__in=self.open_reports())
        ).distinct()


class DentistReportManager(models.Manager):
    def get_queryset(self):
        return DentistReportQureySet(self.model, using=self._db)


# Dentist report model
class DentistReport(DateTimeAuditModel):

    report_title = models.CharField(max_length=300)
    history = models.TextField(blank=True, null=True)
    clinical_finding = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    general_comments = models.TextField(blank=True, null=True)
    closed = models.BooleanField(default=False)

    # ---- Related models ----
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='dentistreport_patient'
    )
    dentist = models.ForeignKey(
        Dentist,
        null=True,
        on_delete=models.SET_NULL,
        related_name='dentistreport_dentist'
    )
    branch = models.ForeignKey(
        Branch,
        null=True,
        on_delete=models.SET_NULL,
        related_name='dentistreport_branch'
    )
    insurance = models.ForeignKey(
        PatientInsurance,
        null=True,
        on_delete=models.SET_NULL,
        related_name='dentistreport_insurance'
    )
    appointment = models.ForeignKey(
        PatientAppointment,
        null=True,
        on_delete=models.SET_NULL,
        related_name='dentistreport_appointment'
    )
    visit = models.ForeignKey(
        PatientVisit,
        on_delete=models.CASCADE,
        related_name='dentistreport_visit'
    )
    updated_by = models.ForeignKey(
        Employee,
        null=True,
        on_delete=models.SET_NULL,
        related_name='dentistreport_updatedby'
    )

    objects = models.Manager()
    allreports = DentistReportManager()

    def __str__(self):
        return self.report_title

    class Meta(DateTimeAuditModel.Meta):
        ordering = ['-created']
        verbose_name = 'Dentist Report'
        verbose_name_plural = 'Dentists Reports'
