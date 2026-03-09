from django.db import models
from django.utils.translation import gettext_lazy as _

from .auxiliary_models import DateTimeAuditModel
from accounts.models import AccountUser
from mimascompany.models.dentist_model import Dentist
from mimascompany.models.employee_model import Employee


# ---- Patient model queryset
class PatientQuerySet(models.QuerySet):
    def to_dentist(self, dentist_id):
        return self.filter(primary_dentist_id=dentist_id)

    def has_dentist(self):
        return self.exclude(primary_dentist__isnull=True)

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
        return self.get_queryset().filter(primary_dentist__employee=employee)


class PatientWithoutDetailsManager(models.Manager):
    """ Get patients without details """
    def without_details(self):
        return self.filter(patientdetail_patient__isnull=True)


class PatientWithoutContactManager(models.Manager):
    """ Get patients without contact """
    def without_contact(self):
        return self.filter(patientcontact_patient__isnull=True)


class PatientWithoutInsuranceManage(models.Manager):
    def without_insurance(self):
        return self.filter(patientinsurance_patient__isnull=True)


# --------------------------- Patients model ----------------------------------

class Patient(DateTimeAuditModel):

    class Gender(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')
        OTHER = 'O', _('Other')
        NOT_SPECIFIED = 'NS', _('Not Specified')

    # ---- Personal info ----
    first_name = models.CharField(max_length=70)
    last_name = models.CharField(max_length=70)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        choices=Gender.choices,
        default=Gender.NOT_SPECIFIED
    )
    patient = models.ForeignKey(
        AccountUser,
        on_delete=models.CASCADE,
        related_name='patient_accountuser'
    )

    # ---- Dentist info ----
    primary_dentist = models.ForeignKey(
        Dentist,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='patients_primarydentist'
    )

    # ---- Audit info ----
    updated_by = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        blank=True, null=True,
        related_name='patients_updatedby'
    )

    # ---- Managers ----
    objects = models.Manager()
    patient_manager = PatientManager()
    patient_without_details = PatientWithoutDetailsManager()
    patient_without_contact = PatientWithoutContactManager()
    patient_without_insurance = PatientWithoutInsuranceManage()

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
        ordering = ['created']
        verbose_name = _("Patient")
        verbose_name_plural = _("Patients")
