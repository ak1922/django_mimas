from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class UserType(models.TextChoices):
    """ User types for default groups created with signal """

    PATIENT = 'Patients', _('Patients')
    DENTIST = 'Dentists', _('Dentists')
    EMPLOYEE = 'Employees', _('Employees')
    ADMINISTRATOR = 'Administrators', _('Administrators')


class AccountUser(AbstractUser):
    """ Main model for all app users """

    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=200, unique=True)
    password = models.CharField()
    user_type = models.CharField(max_length=30, choices=UserType.choices, default=UserType.PATIENT)

    @property
    def is_administrator(self):
        return self.is_superuser

    @property
    def is_employee(self):
        return self.user_type == UserType.EMPLOYEE

    @property
    def is_dentist(self):
        return self.user_type == UserType.DENTIST

    @property
    def is_patient(self):
        return self.user_type == UserType.PATIENT

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
