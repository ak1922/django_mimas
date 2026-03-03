from django.db import models

from .auxiliary_models import AuditModel
from .employee_model import Employee


# Model to manage departments
class Department(AuditModel):

    department_id = models.IntegerField(primary_key=True)
    department_name = models.CharField(max_length=100)
    description = models.TextField()

    department_head = models.ForeignKey(
        Employee,
        null=True,
        on_delete=models.SET_NULL,
        related_name='department_departmenthead'
    )

    class Meta:
        ordering = ['department_name']
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.department_name
