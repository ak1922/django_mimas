from django.db import models

from .auxiliary_models import AuditModel


# Model for services mgmt
class Service(AuditModel):

    service_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    duration = models.IntegerField(null=True, blank=True)

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True, blank=True
    )
    department = models.ForeignKey(
        'mimascompany.Department',
        on_delete=models.CASCADE,
        related_name='service_department'
    )

    def __str__(self):
        return f'{self.service_name}'

    class Meta(AuditModel.Meta):
        ordering = ['service_name']
        db_table = 'services'
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
