from django.db import models

from .auxiliary_models import AuditModel

class PatientBooking(AuditModel):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=250)
    username = models.CharField(
        max_length=10,
        blank=True, null=True
    )

    message = models.TextField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta(AuditModel.Meta):
        ordering = ['-created']
        db_table = 'patient_booking'
        verbose_name = 'Patient Booking'
        verbose_name_plural = 'Patients Bookings'
        indexes = [
            models.Index(fields=['email'], name='pbk_email_idx')
        ]
