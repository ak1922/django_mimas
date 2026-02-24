from django.db import models
from django.conf import settings


# All purpose audit model
class AuditModel(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=True, null=True,
        related_name='%(app_label)s_%(class)s_updated'
    )

    class Meta:
        abstract = True
