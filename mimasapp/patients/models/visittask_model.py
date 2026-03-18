from django.db import models

from mimascompany.models import Employee
from patients.models import PatientVisit, PatientAppointment, DateTimeAuditModel


# Visit management
class PatientVisitTask(DateTimeAuditModel):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In_Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    ]

    class Priority(models.TextChoices):
        LOW = 'Low', 'Low'
        MEDIUM = 'Medium', 'Medium',
        HIGH = 'High', 'High',
        CRITICAL = 'Critical', 'Critical'

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
    appointment = models.ForeignKey(
        PatientAppointment,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='patientvisittask_appointment'
    )
    visit = models.ForeignKey(
        PatientVisit,
        on_delete=models.CASCADE,
        related_name='patientvisittask_visit'
    )
    updated_by = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='patientvisittask_updatedby'
    )

    def __str__(self):
        return f'{self.task_title}- {self.visit.visit_title}'

    class Meta(DateTimeAuditModel.Meta):
        ordering = ['task_status']
        db_table = 'patients_visits_tasks'
        verbose_name = 'Patient Visit Task'
        verbose_name_plural = 'Patients Visits Tasks'
        indexes = [
            models.Index(fields=['assigned_to', 'visit'], name='pvt_assignedtovisit_idx'),
            models.Index(fields=['visit', 'task_status'], name='pvt_visittaskstatus_idx'),
            models.Index(fields=['assigned_to', 'task_title'], name='pvt_assignedtotasktitle_idx')
        ]
