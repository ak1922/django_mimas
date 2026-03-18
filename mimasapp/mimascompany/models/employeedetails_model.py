from django.db import models

from mimascompany.models import Employee, AuditModel, Department


# Model for employee details
class EmployeeDetail(AuditModel):

    class MaritalStatus(models.TextChoices):
        SINGLE = 'SG', 'Single'
        MARRIED = 'MD', 'Married'
        DIVORCED = 'DV', 'Divorced'
        SEPERATED = 'SP', 'Seperated'

    # ---- Employee info ----
    ssn = models.CharField(max_length=14)
    address = models.CharField(max_length=80)
    phone_number = models.CharField(max_length=14)
    date_hired = models.DateField(null=True, blank=True)

    # ---- Spouse info ----

    spouse_name = models.CharField(
        max_length=60,
        null=True, blank=True
    )
    spouse_address = models.CharField(
        max_length=80,
        null=True, blank=True
    )
    spouse_employer = models.CharField(
        max_length=30,
        null=True, blank=True
    )
    spouse_employer_address = models.CharField(
        max_length=80,
        null=True, blank=True
    )
    marital_status = models.CharField(
        max_length=2,
        choices=MaritalStatus.choices,
    )

    # ---- ForeignKey fields ----
    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name='employeedetail_employee'
    )
    supervisor = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='employeedetail_supervisor'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='employeedetail_department'
    )

    @property
    def employee_name(self):
        return f'{self.employee.full_name()}'

    def __str__(self):
        return self.employee.full_name

    class Meta:
        ordering = ['-created', 'employee']
        db_table = 'employee_details'
        verbose_name = 'Employee Detail'
        verbose_name_plural = 'Employee Details'
        indexes = [
            models.Index(fields=['employee', 'department'], name='ed_empdepart_idx'),
            models.Index(fields=['employee', 'supervisor'], name='ed_empsuper_idx'),
            models.Index(fields=['employee', 'marital_status'], name='ed_employeemarital_idx')
        ]
