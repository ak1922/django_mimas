from django.db import models

from .branch_model import Branch
from .employee_model import Employee
from .auxiliary_models import AuditModel

# Dentist model
class Dentist(AuditModel):

    specialty = models.CharField()

    employee = models.OneToOneField(
        Employee,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name='dentist_employee'
    )
    branch_name = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='dentist_branchname'
    )
    supervisor = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='dentist_supervisor'
    )

    @property
    def dentist_name(self):
        return f'{self.employee.full_name}'

    def __str__(self):
        return f'{self.dentist_name}'
