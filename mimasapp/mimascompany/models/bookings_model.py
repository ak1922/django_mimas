from django.db import models

from .auxiliary_models import AuditModel

class PatientBooking(AuditModel):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=250)
    message = models.TextField()
    username = models.CharField(
        max_length=10,
        blank=True, null=True
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
