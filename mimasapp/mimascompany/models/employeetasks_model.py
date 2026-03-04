from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


from .employee_model import Employee
from .auxiliary_models import AuditModel

# Task category model
class TaskCategory(AuditModel):
    """
        Manage categories of employee tasks e.g. clinic tasks, patient tasks,
        corporate tasks, vacation tasks, etc
    """

    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name = 'Task Category'
        verbose_name_plural = 'Task Categories'

    def __str__(self):
        return self.name


# ---- Custom QuerySet for Complex Filters ----
class EmployeeTaskQuerySet(models.QuerySet):
    def active(self):
        """Returns tasks that are not completed or cancelled."""
        return self.exclude(status__in=[EmployeeTask.Status.COMPLETED, EmployeeTask.Status.CANCELLED])

    def over_due(self):
        """Returns active tasks where the end_date has passed."""
        return self.active().filter(end_date__lt=timezone.now())

    def critical_priority(self):
        return self.filter(priority=EmployeeTask.Priority.CRITICAL)


# ---- Custom Manager ----
EmployeeTaskManager = models.Manager.from_queryset(EmployeeTaskQuerySet)


# Employee tasks model
class EmployeeTask(AuditModel):
    """ Manage employee tasks """

    # ---- Priority choices ----
    class Priority(models.IntegerChoices):
        LOW = 1, 'Low'
        MEDIUM = 2, 'Medium'
        HIGH = 3, 'High'
        CRITICAL = 4, 'Critical'

    # ---- Status choices ----
    class Status(models.TextChoices):
        BACKLOG = 'BL', 'Backlog'
        TODO = 'TD', 'To Do'
        IN_PROGRESS = 'IP', 'In Progress'
        COMPLETED = 'CO', 'Completed'
        CANCELLED = 'CA', 'Cancelled'

    # Task info
    task_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    # ---- Dates ----
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)

    # ---- Enum-based fields ----
    priority = models.IntegerField(choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField(choices=Status.choices, default=Status.TODO, max_length=2)


    # ---- ForignKey Columns ------
    category = models.ForeignKey(
        TaskCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='employeetask_category'
    )
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='employeetask_employee'
    )

    # ---- Managers ----
    objects = models.Manager()
    tasks = EmployeeTaskManager()

    class Meta:
        verbose_name = 'Employee Task'
        verbose_name_plural = 'Employee Tasks'
        ordering = ['-priority', 'end_date']
        indexes = [
            models.Index(fields=['status', 'employee'])
        ]

    def __str__(self):
        return f'{self.task_name}'

    def clean(self):
        """Custom validation to ensure end_date is after start_date"""
        super().clean()
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError({'end_date': 'End date cannot be before start date.'})

    @property
    def is_overdue(self):
        """Returns True if task is not completed and end_date has passed"""
        return self.status != self.Status.COMPLETED and timezone.now() > self.end_date


class EmployeeTaskItem(AuditModel):

    # ---- Item info ----
    item_name = models.CharField(max_length=250)
    comments = models.CharField(blank=True, null=True)

    # ---- Dates ----
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    # ---- Foriegn keys ----
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='employeetaskitem_employee'
    )
    task_name = models.ForeignKey(
        EmployeeTask,
        on_delete=models.CASCADE,
        related_name='employeetaskitem_taskname'
    )

    class Meta:
        ordering = ['start_date']
        verbose_name = 'Employee Task Item'
        verbose_name_plural = 'Employee Task Items'

    def __str__(self):
        return f'{self.item_name} - {self.task_name}'
