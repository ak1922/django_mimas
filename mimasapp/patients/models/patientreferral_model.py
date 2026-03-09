from django.db import models

from .patients_model import Patient
from .patientinsurance_model import PatientInsurance
from .patientappointment_model import PatientAppointment
from .patientvisit_models import PatientVisit
from .auxiliary_models import DateTimeAuditModel
from mimascompany.models.dentist_model import Dentist
from mimascompany.models.branch_model import Branch
from mimascompany.models.employee_model import Employee


# ------- Custom referral queryset ----
class PatientReferralQuerySet(models.QuerySet):

    def open_referrals(self):
        return self.filter(closed=False)

    def closed_referrals(self):
        return self.filter(closed=True)

    def dentists_with_openreferrals(self):
        return Dentist.objects.filter(
            patientreferral_dentist__in=self.open_referrals()
        ).distinct()


# ------ Custom manager -------
class PatientReferralManager(models.Manager):

    def get_queryset(self):
        return PatientReferralQuerySet(self.model, using=self._db)

    def open_referrals(self):
        return self.get_queryset().open_referrals()

    def closed_referrals(self):
        return self.get_queryset().closed_referrals()

    def dentist_open_referrals(self):
        return self.get_queryset().dentists_with_openreferrals()


# Patient referral
class PatientReferral(DateTimeAuditModel):

    referral_title = models.CharField(max_length=300)
    referral_date = models.DateField(blank=True, null=True)
    referral_phone = models.CharField(blank=True, null=True)
    reason = models.CharField(blank=True, null=True)
    extra_details = models.TextField()
    closed = models.BooleanField(default=False)

    # ---- Related models ----
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='patientreferral_patient'
    )
    dentist = models.ForeignKey(
        Dentist,
        on_delete=models.SET_NULL,
        null=True,
        related_name='patientreferral_dentist'
    )
    branch = models.ForeignKey(
        Branch,
        null=True,
        on_delete=models.SET_NULL,
        related_name='patientreferral_branch'
    )
    insurance = models.ForeignKey(
        PatientInsurance,
        null=True,
        on_delete=models.SET_NULL,
        related_name='patientreferral_insurance'
    )
    appointment = models.ForeignKey(
        PatientAppointment,
        on_delete=models.SET_NULL,
        null=True,
        related_name='patientreferral_appointment'
    )
    visit = models.ForeignKey(
        PatientVisit,
        on_delete=models.CASCADE,
        related_name='patientreferral_visit'
    )
    updated_by = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='patientreferral_updatedby'
    )

    # ---- Managers ----
    objects = models.Manager()
    all_patientreferrals = PatientReferralManager()

    @property
    def closed_visit(self):
        """ Return closed patient visit """
        if self.visit and self.visit.visit_status == 'Closed':
            return True
        return False

    @property
    def is_finalized(self):
        return self.closed or (self.visit and self.visit.visit_status == 'Closed')

    @property
    def needs_attention(self):
        return not self.is_finalized

    def __str__(self):
        return self.referral_title

    class Meta(DateTimeAuditModel.Meta):
        ordering =['created']
        verbose_name = 'Patient Referral'
        verbose_name_plural = 'Patient Referrals'
