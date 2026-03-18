from django.db import models
from django.db.models import Q

from accounts.models import AccountUser
from .auxiliary_models import DateTimeAuditModel
from mimascompany.models import Dentist, Employee


# ---- Patient model queryset
class PatientQuerySet(models.QuerySet):
    def to_dentist(self, dentist_id):
        return self.filter(Q(primary_dentist_id=dentist_id))

    def has_dentist(self):
        return self.exclude(Q(primary_dentist__isnull=True))

    def recently_updated(self):
        return self.order_by('updated')

    def male_patients(self):
        return self.filter(gender=Patient.Gender.MALE)

    def female_patients(self):
        return self.filter(gender=Patient.Gender.FEMALE)


# --------------------------  Custom Patient Managers ------------------------

class PatientManager(models.Manager):
    def get_queryset(self):
        return PatientQuerySet(self.model, using=self._db).select_related('primary_dentist')

    def for_employee(self, employee):
        """ Get patients associated with a specific dentist employee """
        return self.get_queryset().filter(Q(primary_dentist__employee=employee))


class PatientWithoutDetailsManager(models.Manager):
    """ Get patients without details """
    def without_details(self):
        return self.filter(Q(patientdetail_patient__isnull=True))


class PatientWithoutContactManager(models.Manager):
    """ Get patients without contact """
    def without_contact(self):
        return self.filter(Q(patientcontact_patient__isnull=True))


class PatientWithoutInsuranceManage(models.Manager):
    def without_insurance(self):
        return self.filter(Q(patientinsurance_patient__isnull=True))


# --------------------------- Patients model ----------------------------------

class Patient(DateTimeAuditModel):

    class Gender(models.TextChoices):
        MALE = 'M', 'Male',
        FEMALE = 'F', 'Female',
        OTHER = 'O', 'Other',
        NOT_SPECIFIED = 'NS', 'Not Specified',

    # ---- Personal info ----
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        choices=Gender.choices,
        default=Gender.NOT_SPECIFIED
    )

    # ---- Related models ----
    patient = models.ForeignKey(
        AccountUser,
        on_delete=models.CASCADE,
        related_name='patient_accountuser'
    )
    primary_dentist = models.ForeignKey(
        Dentist,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='patients_primarydentist'
    )
    updated_by = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        blank=True, null=True,
        related_name='patients_updatedby'
    )

    # ---- Managers ----
    objects = models.Manager()
    patient_manager = PatientManager()
    withoutdetails = PatientWithoutDetailsManager()
    withoutcontact = PatientWithoutContactManager()
    withoutinsurance = PatientWithoutInsuranceManage()

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def patient_username(self):
        return self.patient.username

    @property
    def patient_dentistname(self):
        return self.primary_dentist.dentist_name if self.primary_dentist else 'No Dentist Assigned'

    @property
    def has_contact(self):
        return self.patientcontact_patient if self.patientcontact_patient else 'No Contacts'

    @property
    def has_detail(self):
        return self.patientdetail_patient if self.patientdetail_patient else 'No Details'

    @property
    def has_insurance(self):
        return self.patientinsurance_patient if self.patientinsurance_patient else 'No Insurance'

    @property
    def has_appointment(self):
        return self.patientappointment_patient if self.patientappointment_patient else 'No Appointment/s'

    def __str__(self):
        return self.full_name

    class Meta(DateTimeAuditModel.Meta):
        ordering = ['-created']
        db_table = 'patients'
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        indexes = [
            models.Index(fields=['patient', 'gender'], name='p_patientgender_idx'),
            models.Index(fields=['patient', 'primary_dentist'], name='p_patientprimdentist_idx'),
        ]
