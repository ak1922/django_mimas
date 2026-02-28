from django.db import models

from .service_model import Service
from .employee_model import Employee
from .auxiliary_models import AuditModel
from .department_model import Department


# Model for managing branches
class Branch(AuditModel):

    # ---- Branch info
    branch_name = models.CharField(max_length=50)
    location = models.CharField(
        max_length=150,
        blank=True, null=True
    )

    # ---- Many2Many fields
    departments = models.ManyToManyField(
        Department,
        related_name='branch_departments'
    )
    services = models.ManyToManyField(
        Service,
        related_name='branch_services'
    )

    # ---- ForeignKey fields
    branch_head = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='branch_branchhead'
    )

    class Meta:
        ordering = ['branch_name']
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'

    def __str__(self):
        return f'{self.branch_name}'
