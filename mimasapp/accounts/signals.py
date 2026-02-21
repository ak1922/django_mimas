from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.db.models.signals import post_save

from .models import AccountUser


# ------- User Group Assigment --------
@receiver(post_save, sender=AccountUser)
def assign_user_group(sender, instance, created, **kwargs):
    """ Assign users to a group after registration """

    if created:
        if instance.is_superuser:
            group, _ = Group.objects.get_or_create(name='Administrators')
            instance.groups.add(group)

        elif instance.is_employee:
            group, _ = Group.objects.get_or_create(name='Employees')
            instance.groups.add(group)

        elif instance.is_dentist:
            group, _ = Group.objects.get_or_create(name='Dentists')
            instance.groups.add(group)

        else:
            group, _ = Group.objects.get_or_create(name='Patients')
            instance.groups.add(group)
