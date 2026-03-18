import os
from PIL import Image
from django.db import models
from model_utils import Choices
from django.db.models import Sum

from accounts.models import AccountUser
from mimascompany.models import  AuditModel
from .leaverequests_model import LeaveRequest

def photo_store(instance, filename):

    upload_to = 'pictures'
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(instance.user.username, ext)
    return os.path.join(upload_to, filename)


# Staff positions
class CompanyPositions(AuditModel):

    title = models.CharField(max_length=200, unique=True)
    description = models.CharField()

    class Meta:
        db_table = 'company_positions'
        ordering = ['title']
        verbose_name = "Company Position"
        verbose_name_plural = "Company Positions"

    def __str__(self):
        return self.title


# Custom model manager
class EmployeeManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(status=Employee.EmployeeStatus.ACTIVE)

    def terminted(self):
        return self.get_queryset().filter(status=Employee.EmployeeStatus.TERMINATED)

    def on_vacation(self):
        return self.get_queryset().filter(status=Employee.EmployeeStatus.VACATION)

    def on_absence(self):
        return self.get_queryset().filter(status=Employee.EmployeeStatus.LEAVE_OF_ABSENCE)

    def on_suspension(self):
        return self.get_queryset().filter(status=Employee.EmployeeStatus.SUSPENDED)


# Employee model
class Employee(AuditModel):
    """ Main employees model """

    class EmployeeStatus(models.TextChoices):
        """ Employee statuses in company """
        ACTIVE = 'AC', 'Active'
        INACTIVE = 'IAC', 'Inactive'
        LEAVE_OF_ABSENCE = 'LOA', 'Leave Of Absence'
        VACATION = 'VC', 'Vacation'
        TERMINATED = 'TMD', 'Terminated'
        SUSPENDED = 'SUP', 'Suspended'

    GENDER_CHOICES = Choices(
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    # ------------ Personal Info ----
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=200)
    photo = models.ImageField(
        upload_to='photo_store',
        blank=True, null=True
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )
    status = models.CharField(
        choices=EmployeeStatus.choices,
        default=EmployeeStatus.ACTIVE
    )
    vacations_days_accrued = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.0
    )

    # ---- Relational fields ----
    user = models.OneToOneField(
        AccountUser,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name='employee_accountuser'
    )
    position = models.ForeignKey(
        CompanyPositions,
        on_delete=models.PROTECT,
        blank=True, null=True,
        related_name='employee_companypositions'
    )

    # ---------- Managers ----------
    objects = models.Manager()
    active_employees = EmployeeManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.photo:
            img = Image.open(self.photo.path)
            output_size = (300, 300)
            img = img.resize(output_size, Image.Resampling.LANCZOS)
            img.save(self.photo.path)
        else:
            print('No user photo uploaded with profile.')

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def employee_username(self):
        return f'{self.user.username}'

    @property
    def employee_with_details(self):
        if self.employeedetail_employee:
            return True
        return False

    @property
    def employee_with_contact(self):
        if self.employeecontact_employee:
            return True
        return False

    @property
    def vacation_days_remaining(self):
        """ Calculate vacation days taken """

        vacation_code = LeaveRequest.LeaveType.choices.VACATION
        used_days = self.employee_leaverequest.filter(
            leave_type__code=vacation_code,
            status=LeaveRequest.ApprovalStatus.APPROVED
        ).aggregate(Sum('days_taken'))['days_taken__sum'] or 0
        return self.vacations_days_accrued - used_days

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.position or 'No Position'})'

    class Meta:
        ordering = ['last_name', 'first_name']
        db_table = 'employees'
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        indexes = [
            models.Index(fields=['user', 'status'], name='e_userstatus_idx'),
            models.Index(fields=['user', 'gender'], name='e_usergender_idx'),
        ]
