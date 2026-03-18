from django.db import models
from django.db.models import Index
from model_utils import FieldTracker
from django.core.exceptions import ValidationError

from mimascompany.models import Branch, Service, Dentist, Employee, Department
from patients.models import Patient, PatientInsurance, PatientAppointment, DateTimeAuditModel
from .treatmentroom_model import TreatmentRoom


POST_VISIT_CHOICES = [
    ('Lab', 'Lab'),
    ('Referral', 'Referral'),
    ('Treatment', 'Treatment'),
    ('Dentist Report', 'Dentist Report')
]


class PostVisitOption(models.Model):
    name = models.CharField(max_length=50, choices=POST_VISIT_CHOICES, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Post Visit Option'
        verbose_name_plural = 'Posts Visits Options'


# --- Custom Manager ---
class VisitManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def completed(self):
        """Custom method to get only completed visits"""
        return self.get_queryset().filter(status='Completed')


# Patient visit model
class PatientVisit(DateTimeAuditModel):

    VISIT_STATUS = [
        ('Created','Created'),
        ('Checked In','Checked In'),
        ('Completed','Completed'),
        ('Closed','Closed'),
        ('No Show','No Show'),
    ]

    VISIT_TIME = [
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

    # ---- Visit info ----
    visit_title = models.CharField(max_length=300)
    visit_date = models.DateField()
    visit_time = models.CharField(
        choices=VISIT_TIME,
        blank=True, null=True,
        max_length=10
    )
    visit_status = models.CharField(
        choices=VISIT_STATUS,
        default='Created',
        max_length=15
    )

    # ---- Related models ----
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='patientvisit_patient'
    )
    dentist = models.ForeignKey(
        Dentist,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='patientvisit_dentist'
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='patientvisit_branch'
    )
    insurance = models.ForeignKey(
        PatientInsurance,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='patientvisit_insurance'
    )
    appointment = models.OneToOneField(
        PatientAppointment,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='patientvisit_appointment'
    )
    updated_by = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='patientvisit_updatedby'
    )
    treatment_room = models.ForeignKey(
        TreatmentRoom,
        on_delete=models.SET_NULL,
        default=None,
        blank=True, null=True,
        related_name='patientvisit_treatmentroom'
    )

    # ---- Many2Many fields ----
    services = models.ManyToManyField(
        Service,
        related_name='patientvisit_services'
    )
    departments = models.ManyToManyField(
        Department,
        related_name='patientvisit_departments'
    )
    visit_options = models.ManyToManyField(
        PostVisitOption,
        related_name='patientvisit_visitoptions'
    )

    tracker = FieldTracker(fields=['visit_options', 'visit_status'])

    # ---- Managers ----
    objects = models.Manager()
    visits = VisitManager()

    def clean(self):
        super().clean()
        if self.branch and self.treatment_room and self.branch.branch_name != self.treatment_room.branch.branch_name:
            raise ValidationError('There is a mismatch between Branch and Treatment Room')

    def save(self, *args, **kwargs):
        if not kwargs.pop('skip_validation', False):
            self.full_clean()
        super().save(*args, **kwargs)

    @property
    def all_treatments_closed(self):
        treatments = self.patienttreatment_visit.all()
        if not treatments.exists():
            return True
        return not treatments.filter(closed=False).exists()

    @property
    def open_treatments(self):
        return self.patienttreatment_visit.filter(closed=False)

    @property
    def open_treatments_count(self):
        return self.open_treatments.count()

    @property
    def all_referrals_closed(self):
        referrals = self.patientreferral_visit.all()
        if not referrals.exists():
            return True
        return not referrals.filter(closed=False).exists()

    @property
    def open_referrals(self):
        return self.patientreferral_visit.filter(closed=False)

    @property
    def open_referrals_count(self):
        return self.open_referrals.count()

    @property
    def all_labs_closed(self):
        labs = self.patientlab_visit.all()
        if not labs.exists():
            return True
        return not labs.filter(closed=False).exists()

    @property
    def open_labs(self):
        return self.patientlab_visit.filter(closed=False)

    @property
    def open_labs_count(self):
        return self.open_labs.count()

    @property
    def all_closed_reports(self):
        dentistreports = self.dentistreport_visit.all()
        if not dentistreports.exists():
            return True
        return not dentistreports.filter(closed=False).exists()

    @property
    def open_reports(self):
        return self.dentistreport_visit.filter(closed=False)

    @property
    def open_reports_count(self):
        return self.open_reports.count()

    @property
    def allpaid_bills(self):
        bill = getattr(self, 'patientbill_visit', None)
        if bill:
            return bill.is_paid
        return True

    def __str__(self):
        return f'{self.visit_title}'

    class Meta(DateTimeAuditModel.Meta):
        db_table = 'patient_visits'
        ordering = ['-visit_date', '-visit_time']
        verbose_name = 'Patient Visit'
        verbose_name_plural = 'Patients Visits'
        indexes = [
            Index(fields=['visit_date'], name='visit_date_idx'),
            Index(fields=['visit_status'], name='visit_status_idx'),
            Index(fields=['patient', 'visit_date'], name='patient_visitdate_idx'),
            Index(fields=['dentist', 'visit_status'], name='dentist_visitstatus_idx')
        ]
