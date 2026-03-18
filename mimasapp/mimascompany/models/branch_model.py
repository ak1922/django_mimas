from django.db import models

from mimascompany.models import Employee, AuditModel


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
        'mimascompany.Department',
        related_name='branch_departments'
    )
    services = models.ManyToManyField(
        'mimascompany.Service',
        related_name='branch_services'
    )

    # ---- ForeignKey fields
    branch_head = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='branch_branchhead'
    )

    def __str__(self):
        return f'{self.branch_name}'

    class Meta(AuditModel.Meta):
        ordering = ['branch_name']
        db_table = 'branches'
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'
        indexes = [
            models.Index(fields=['location'], name='b_location_idx')
        ]
