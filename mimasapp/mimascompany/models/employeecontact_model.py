from django.db import models

from .employee_model import Employee
from .auxiliary_models import AuditModel

# Employee contact
class EmployeeContact(AuditModel):

    # ---- Employee info ----
    contact_name = models.CharField(max_length=100)
    contact_address = models.CharField(max_length=150)
    contact_phone = models.CharField(max_length=14)
    relationship = models.CharField(max_length=20)

    # ---- ForeinKey fields ----
    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='employeecontact_employee'
    )

    @property
    def employee_name(self):
        return f'{self.employee.full_name}'

    class Meta:
        ordering = ['contact_name']
        verbose_name = 'EmployeeContact'
        verbose_name_plural = 'EmployeeContacts'

    def __str__(self):
        return f'Emergency Contact: {self.employee_name}'
