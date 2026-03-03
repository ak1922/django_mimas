from django.db import models

from .auxiliary_models import AuditModel
from .employee_model import Employee
from .department_model import Department


# Model for services mgmt
class Service(AuditModel):

    service_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='service_department')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.service_name}'
