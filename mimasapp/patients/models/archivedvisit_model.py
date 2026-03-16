from django.db import models

from mimascompany.models import Employee, Branch, Dentist, Department, Service
from patients.models import Patient, PatientInsurance, PostVisitOption


# Archived visit
class ArchivedPatientVisit(models.Model):

    visit_date = models.DateField()
    visit_status = models.CharField(max_length=15)
    visit_time = models.CharField(
        max_length=10,
        blank=True, null=True
    )

    archived = models.DateTimeField(null=True, blank=True)
    updated = models.DateTimeField(blank=True, null=True)

    visit_title = models.CharField(
        unique=True,
        max_length=300
    )
    total_price_aggregated = models.DecimalField(
        blank=True, null=True,
        max_digits=10, decimal_places=2
    )

    # ---- ForeignKeys ----
    patient = models.ForeignKey(
        Patient,
        on_delete=models.SET_NULL,
        null=True,
        related_name='archivedpatientvisit_patient'
    )
    dentist = models.ForeignKey(
        Dentist,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedpatientvisit_dentist'
    )
    branch = models.ForeignKey(
        Branch,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedpatientvisit_branch'
    )
    insurance = models.ForeignKey(
        PatientInsurance,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedpatientvisit_insurance'
    )
    appointment = models.ForeignKey(
        'patients.ArchivedPatientAppointment',
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedpatientvisit_appointment'
    )
    updated_by = models.ForeignKey(
        Employee,
        null=True,
        on_delete=models.SET_NULL,
        related_name='archivedpatientvisit_updatedby'
    )

    # ----- Many2Many fields -------
    departments = models.ManyToManyField(
        Department,
        blank=True,
        related_name='archivedpatientvisit_department'
    )
    services = models.ManyToManyField(
        Service,
        blank=True,
        related_name='archivedpatientvisit_services'
    )
    visit_options = models.ManyToManyField(
        PostVisitOption,
        blank=True,
        related_name='archivedpatientvisit_visitoptions'
    )

    @property
    def visit_department_names(self):
        return ', '.join(self.departments.values_list('department_name', flat=True))

    @property
    def visit_service_names(self):
        return ', '.join(self.services.values_list('service_name', flat=True))

    @property
    def visit_postoption_names(self):
        return ', '.join(self.visit_options.values_list('name', flat=True))

    def __str__(self):
        return self.visit_title

    class Meta:
        db_table = 'archived_patient_visit'
        verbose_name = 'Archived Patient Visit'
        verbose_name_plural = 'Archived Patients Visits'
