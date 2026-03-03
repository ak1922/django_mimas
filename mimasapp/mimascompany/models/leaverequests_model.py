from django.db import models
from django.conf import settings

from .auxiliary_models import AuditModel

# Custom model manager
class LeaveRequestManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('employee', 'approved_by')

    def pending(self):
        return self.filter(status=LeaveRequest.ApprovalStatus.PENDING)

    def approved(self):
        return self.filter(status=LeaveRequest.ApprovalStatus.APPROVED)

    def for_employee(self, employee):
        return self.filter(employee=employee)

    def get_active_leave(self, employee, current_date):
        return self.approved().filter(
            employee=employee,
            start_date__lte=current_date,
            end_date__gte=current_date
        )


# Employee leave model
class LeaveRequest(AuditModel):
    """ Manage employee vacations and leave """

    class ApprovalStatus(models.TextChoices):
        PENDING = 'P', 'Pending'
        APPROVED = 'A', 'Approved'
        DENIED = 'D', 'Denied'

    class LeaveType(models.TextChoices):
        PIAD_DAY_OFF = 'PDO', 'Paid Day Off'
        UNPAID_DAY_OFF = 'UDO', 'Unpaid Day Off'
        VACATION = 'VCA', 'Vacation'
        MEDICAL_LEAVE = 'ML', 'Medical Leave'

    start_date = models.DateField()
    end_date = models.DateField()
    requested_date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(blank=True)

    days_taken = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        blank=True, null=True
    )
    leave_type = models.CharField(
        max_length=5,
        choices=LeaveType.choices
    )
    status = models.CharField(
        max_length=1,
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.PENDING
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='approved_leave_requests'
    )
    employee = models.ForeignKey(
        'Employee',
        on_delete=models.CASCADE,
        related_name='employee_leaverequest'
    )

    # ----------------- Model managers --------------------
    objects = models.Manager()
    leavedays = LeaveRequestManager()

    class Meta:
        ordering = ['status']
        verbose_name = 'EmployeeDetail'
        verbose_name_plural = 'EmployeeDetails'

    def __str__(self):
        return f"{self.employee.full_name}"
