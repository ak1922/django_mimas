from django.db import models
from django.db.models import Max
from django.utils.text import slugify
from django.template.defaultfilters import upper

from .auxiliary_models import DateTimeAuditModel
from mimascompany.models import Branch, Employee


# ---- Custom manager ------
class TreatmentRoomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('visit', 'branch')

    def is_available(self):
        return self.get_queryset().filter(is_occupied=False)

    def occupied(self):
        return self.get_queryset().filter(is_occupied=True)


class TreatmentRoom(DateTimeAuditModel):

    is_occupied = models.BooleanField(default=False)
    room_name = models.CharField(
        unique=True,
        max_length=200
    )
    room_number = models.CharField(
        max_length=50,
        unique=True,
        null=True, blank=True
    )

    # An IntegerField to hold the auto-incrementing part for a specific branch
    room_index = models.PositiveIntegerField(default=1, null=True, blank=True)

    # ---- Related models ----
    visit = models.ForeignKey(
        'patients.PatientVisit',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='treatmentroom_visit'
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        related_name='treatmentroom_branch'
    )
    updated_by = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='treatmentroom_updatedby'
    )

    # ---- Managers ----
    objects = models.Manager()
    treatments = TreatmentRoomManager()

    def save(self, *args, **kwargs):
        if not self.room_number:
            last_room = TreatmentRoom.objects.filter(branch=self.branch).aggregate(Max('room_index'))
            next_index = (last_room['room_index__max'] or 0 ) + 1
            self.room_index = next_index
            self.room_number = f'{upper(slugify(self.branch.branch_name))}-{next_index:03d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.room_name} - {self.branch.branch_name}'

    class Meta(DateTimeAuditModel.Meta):
        ordering = ['room_name', 'updated']
        verbose_name = 'Treatment Room'
        verbose_name_plural = 'Treatment Rooms'
        constraints = [
            models.UniqueConstraint(
                name='branch_room_constraint',
                fields=['room_name', 'branch'],
                violation_error_message='The room chosen belongs to a different branch.'
            )
        ]
