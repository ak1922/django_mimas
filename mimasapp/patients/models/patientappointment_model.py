from django.db import models
from django.db.models import Manager
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import time, datetime, timedelta

from accounts.models import AccountUser
from mimascompany.models import Dentist, Branch, Employee
from patients.models import Patient, PatientInsurance, DateTimeAuditModel


# Custom manager class
class ConfirmedAppointmentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=AppointmentStatus.CONFIRMED)

    def upcoming_appointments(self):
        from datetime import date
        return self.get_queryset().filter(appointment_date__gte=date.today())


# Appointment status choices
class AppointmentStatus(models.TextChoices):
    SCHEDULED = 'SCHEDULED', 'Scheduled'
    CONFIRMED = 'CONFIRMED', 'Confirmed'
    CANCELLED = 'CANCELLED', 'Cancelled'
    COMPLETED = 'COMPLETED', 'Completed'
    NO_SHOW = 'NO_SHOW', 'No Show'


# Patient appointment model
class PatientAppointment(DateTimeAuditModel):

    APPOINT_TIME = [
        ('08:00 AM', '08:00 AM'),
        ('09:00 AM', '09:00 AM'),
        ('10:00 AM', '10:00 AM'),
        ('11:00 AM', '11:00 AM'),
        ('12:00 PM', '12:00 PM'),
        ('01:00 PM', '01:00 PM'),
        ('02:00 PM', '02:00 PM'),
        ('03:00 PM', '03:00 PM'),
        ('04:00 PM', '04:00 PM'),
    ]

    # ---- Appointment info ----
    appointment_title = models.CharField(max_length=300)
    reason = models.TextField(max_length=600)
    appointment_date = models.DateField()
    appointment_time = models.CharField(
        max_length=10,
        choices=APPOINT_TIME
    )
    status = models.CharField(
        max_length=20,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.SCHEDULED
    )

    # ---- Related models ----
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='patientappointment_patient'
    )
    dentist = models.ForeignKey(
        Dentist,
        null=True,
        on_delete=models.SET_NULL,
        related_name='patientappointment_dentist'
    )
    branch = models.ForeignKey(
        Branch,
        null=True,
        on_delete=models.SET_NULL,
        related_name='patientappointment_branch'
    )
    insurance = models.ForeignKey(
        PatientInsurance,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='patientappointment_insurance'
    )
    updated_by = models.ForeignKey(
        AccountUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='patientappointment_updatedby'
    )

    # ---- Managers ----
    objects = models.Manager()
    confirmed_appointments = ConfirmedAppointmentManager()

    def clean(self):
        # Match Dentist and Branch
        if self.dentist and self.branch:
            if self.dentist.branch != self.branch:
                raise ValidationError(
                    f'Dentist {self.dentist.dentist_name} does not work at {self.branch}, choose {self.dentist.branch}.'
                )
    #
    #     # Prevent bookings for the same day if it's already 6 PM (18:00) or later.
    #     if self.appointment_date and self.appointment_date == timezone.now().date():
    #         # Define the cutoff time (6 PM)
    #         cutoff_time = time(18, 0, 0)
    #         # Combine appointment date with 6 PM
    #         deadline = timezone.make_aware(datetime.combine(self.appointment_date, cutoff_time))
    #
    #         if timezone.now() > deadline:
    #             raise ValidationError('Cannot book appointments in the past or after 6 PM on the same day.')
    #
    #     # General past date check (prevents picking yesterday)
    #     if self.appointment_date and self.appointment_date < timezone.now().date():
    #         raise ValidationError('Cannot book appointments in the past')
    #
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def confirmed_appointment(self):
        return self.status == AppointmentStatus.CONFIRMED

    @property
    def unconfirmed_within_three_days(self):
        """ Check if appointment is confirmed within 3 days """
        today = timezone.now().date()
        three_days_to = today + timedelta(days=3)
        return (
            self.status == AppointmentStatus.SCHEDULED and
            today <= self.appointment_date <= three_days_to
        )

    def __str__(self):
        return f'{self.patient.full_name} - {self.appointment_title}'

    class Meta(DateTimeAuditModel.Meta):
        db_table = 'patient_appointments'
        ordering = ['-appointment_date', '-appointment_time']
        verbose_name = 'Patient Appointment'
        verbose_name_plural = 'Patient Appointments'
        constraints = [
            models.UniqueConstraint(
                name='DoubleBooking_DentistConstraint',
                fields=['dentist', 'appointment_date', 'appointment_time'],
                violation_error_message='The chosen time is already booked by another appointment.'
            )
        ]
        indexes = [
            models.Index(fields=['-appointment_date'], name='pa_date_idx'),
            models.Index(fields=['-appointment_time'], name='pa_time_idx'),
            models.Index(fields=['branch', 'patient'], name='pa_branchpatient_idx'),
            models.Index(fields=['branch', 'dentist'], name='pa_branchdentist_idx'),
        ]
