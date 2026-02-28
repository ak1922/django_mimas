from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class UserType(models.TextChoices):
    """ User types for default groups created with signal """

    PATIENTS = 'Patients', _('Patients')
    DENTISTS = 'Dentists', _('Dentists')
    EMPLOYEES = 'Employees', _('Employees')
    ADMINISTRATORS = 'Administrators', _('Administrators')


class AccountUser(AbstractUser):
    """ Main model for all app users """

    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    password = models.CharField()
    user_type = models.CharField(max_length=30, choices=UserType.choices, default=UserType.PATIENTS)

    @property
    def is_administrator(self):
        return self.is_superuser

    @property
    def is_employee(self):
        return self.user_type == UserType.EMPLOYEES

    @property
    def is_dentist(self):
        return self.user_type == UserType.DENTISTS

    @property
    def is_patient(self):
        return self.user_type == UserType.PATIENTS

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
