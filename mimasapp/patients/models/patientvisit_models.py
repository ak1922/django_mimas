from django.db import models
from model_utils import FieldTracker

from .auxiliary_models import DateTimeAuditModel
from .patients_model import Patient
from .patientinsurance_model import PatientInsurance
from .patientappointment_model import PatientAppointment
from mimascompany.models.employee_model import Employee
from mimascompany.models.dentist_model import Dentist
from mimascompany.models.branch_model import Branch
from mimascompany.models.service_model import Service
from mimascompany.models.department_model import Department


POST_VISIT_CHOICES = [
    ('Lab', 'Lab'),
    ('Referral', 'Referral'),
    ('Treatment', 'Treatment'),
    ('Dentist Report', 'Dentist Report')
]

# 1. Define the PostVisitOption model first
class PostVisitOption(models.Model):
    name = models.CharField(max_length=50, choices=POST_VISIT_CHOICES, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Post Visit Option'
        verbose_name_plural = 'Posts Visits Options'


# --- Custom Manager ---
class VisitManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def completed(self):
        """Custom method to get only completed visits"""
        return self.get_queryset().filter(status='Completed')


# Patient visit model
class PatientVisit(DateTimeAuditModel):

    class VisitStatus(models.TextChoices):
        CREATED = 'CREATE', 'Created'
        CHECKED_IN = 'CHECK', 'Checked In'
        COMPLETED = 'COMP', 'Completed'
        CLOSED = 'CLOSED', 'Closed'
        NO_SHOW = 'NO SHOW', 'No Show'

    # ---- Visit info ----
    visit_title = models.CharField(max_length=300)
    visit_date = models.DateField()
    visit_time = models.CharField(blank=True, null=True)
    visit_status = models.CharField(choices=VisitStatus.choices)

    # ---- Related models ----
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='patientvisit_patient'
    )
    dentist = models.ForeignKey(
        Dentist,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='patientvisit_dentist'
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='patientvisit_branch'
    )
    insurance = models.ForeignKey(
        PatientInsurance,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='patientvisit_insurance'
    )
    appointment = models.OneToOneField(
        PatientAppointment,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='patientvisit_appointment'
    )
    updated_by = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='patientvisit_updatedby'
    )

    # ---- Many2Many fields ----
    services = models.ManyToManyField(
        Service,
        related_name='patientvisit_services'
    )
    departments = models.ManyToManyField(
        Department,
        related_name='patientvisit_departments'
    )
    visit_options = models.ManyToManyField(
        PostVisitOption,
        related_name='patientvisit_visitoptions'
    )

    tracker = FieldTracker(fields=['visit_options', 'visit_status'])

    # ---- Managers ----
    objects = models.Manager()
    visits = VisitManager()

    def __str__(self):
        return f'{self.visit_title}'

    class Meta(DateTimeAuditModel.Meta):
        ordering = ['-visit_date', '-visit_time']
        verbose_name = 'Patient Visit'
        verbose_name_plural = 'Patients Visits'


# Visit management
class PatientVisitTask(DateTimeAuditModel):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In_Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    ]

    class Priority(models.IntegerChoices):
        LOW = 1, 'Low'
        MEDIUM = 2, 'Medium'
        HIGH = 3, 'High'
        CRITICAL = 4, 'Critical'

    task_title = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    task_status = models.CharField(
        choices=STATUS_CHOICES,
        default='Pending'
    )
    priority = models.CharField(
        choices=Priority.choices,
        default='Medium'
    )

    # ---- Related models ----
    assigned_to = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='patientvisittask_assignedto'
    )
    visit = models.ForeignKey(
        PatientVisit,
        on_delete=models.CASCADE,
        related_name='patientvisittask_visit'
    )

    class Meta(DateTimeAuditModel.Meta):
        ordering = ['task_status']
        verbose_name = 'Patient Visit Task'
        verbose_name_plural = 'Patient Visits Tasks'

    def __str__(self):
        return f'{self.task_title}- {self.visit.visit_title}'
