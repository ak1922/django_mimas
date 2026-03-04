from django.db import models
from django.db.models import Manager
from django.utils import timezone
from django.core.exceptions import ValidationError

from patients.models.auxiliary_models import DateTimeAuditModel
from patients.models.patients_model import Patient
from patients.models.patientinsurance_model import PatientInsurance
from mimascompany.models.employee_model import Employee
from mimascompany.models.dentist_model import Dentist
from mimascompany.models.branch_model import Branch


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
        related_name='patientappointment_branchname'
    )
    insurance = models.ForeignKey(
        PatientInsurance,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='patientappointment_insurance'
    )
    updated_by = models.ForeignKey(
        Employee,
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
        if self.dentist and self.branch_name:
            if self.dentist.branch_name != self.branch_name:
                raise ValidationError(
                    f'Dentist {self.dentist.dentist_name} does not work at {self.branch_name}, choose {self.dentist.branch_name}.'
                )

        # Prevent bookings in the past.
        if self.appointment_date and self.dentist:
            if self.appointment_date < timezone.now().date():
                raise ValidationError('Cannot book appointments in the past')

        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.patient.full_name} - {self.appointment_title}'

    class Meta(DateTimeAuditModel.Meta):
        ordering = ['-appointment_date', '-appointment_time']
        verbose_name = 'Patient Appointment'
        verbose_name_plural = 'Patient Appointments'

        # Model constraints
        constraints = [
            # Prevent double booking
            models.UniqueConstraint(
                name='DoubleBooking_DentistConstraint',
                fields=['dentist', 'appointment_date', 'appointment_time'],
                violation_error_message='The chosen time is already booked by another appointment.'
            )
        ]


# Patient booking model
class PatientBooking(DateTimeAuditModel):

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=300)
    message = models.TextField()

    def person_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.person_name()} - Booking'

    class Meta:
        ordering = ['created']
        verbose_name = 'Patient Booking'
        verbose_name_plural = 'Patient Bookings'
