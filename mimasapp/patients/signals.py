import logging
from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import post_save, m2m_changed, post_delete

from dentists.models.dentistreport_model import DentistReport
from patients.models.patientlab_model import PatientLab
from patients.models.patientreferral_model import PatientReferral
from patients.models.patienttreatment_model import PatientTreatment
from patients.models.patientbill_model import PatientBill
from patients.models.patientvisit_models import PatientVisit, PostVisitOption
from patients.models.patientappointment_model import PatientAppointment, AppointmentStatus
from patients.models.patientmessage_model import PatientMessage
from patients.models.treatmentroom_model import TreatmentRoom
from patients.models.visittask_model import PatientVisitTask

logger = logging.getLogger(__name__)


# Create visit, task and bill
@receiver(post_save, sender=PatientAppointment, dispatch_uid="create_visit_task_bill_signal")
def create_visit_task_bill(sender, instance, created, **kwargs):
    """
    Signal from PatientAppointment to create:
        1. Patient visit
        2. Employee task for patient visit
        3. Bill for patient visit
    """
    logger.info(f'Signal triggered for app: {instance.id}, Status: {instance.status}')

    if instance.status == AppointmentStatus.CONFIRMED:
        if not PatientVisit.objects.filter(appointment=instance).exists():
            if not PatientBill.objects.filter(appointment=instance).exists():
                if not PatientVisitTask.objects.filter(appointment=instance).exists():

                    unique_visit_title = f'{instance.appointment_title} - {instance.id}'

                    # Create patient visit
                    new_visit = PatientVisit.objects.create(
                        patient=instance.patient,
                        dentist=instance.dentist,
                        branch=instance.branch,
                        insurance=instance.insurance,
                        appointment=instance,
                        visit_title=unique_visit_title,
                        visit_date=instance.appointment_date,
                        visit_time=instance.appointment_time,
                    )
                    logger.info(f'New visit created for {instance.patient.full_name}')

                    # Create patient visit bill
                    PatientBill.objects.create(
                        patient=instance.patient,
                        appointment=instance,
                        visit=new_visit,
                        bill_title=f"Bill: {instance}"
                    )
                    logger.info(f'New patient bill created for {new_visit}')

                    # Create visit task
                    PatientVisitTask.objects.create(
                        task_title=unique_visit_title,
                        appointment=instance,
                        visit=new_visit,
                    )
                    logger.info(f'New employee task created for {new_visit}')


# -------------------------- Create post visit options ------------------------------

OPTION_LAB = 'Lab'
OPTION_REPORT = 'Dentist Report'
OPTION_REFERRAL = 'Referral'
OPTION_TREATMENT = 'Treatment'

CHECKED_IN = 'Checked In'
STATUS_COMPLETED = 'Completed'


@receiver(m2m_changed, sender=PatientVisit.visit_options.through)
def track_patient_visit_options(sender, instance, action, pk_set, **kwargs):
    """
    Signal from PatientVisit to track and create visit options
        Referral, Treatment, Lab, Dentist Report
    """

    if action == 'post_add':
        if instance.visit_status != 'CHECKED_IN':
            return

        for option_id in pk_set:
            option = PostVisitOption.objects.get(pk=option_id)

            base_data = {
                'patient': instance.patient,
                'dentist': instance.dentist,
                'branch': instance.branch,
                'insurance': instance.insurance,
                'appointment': instance.appointment,
                'visit': instance
            }

            if option.name == OPTION_LAB:
                if not PatientLab.objects.filter(visit=instance).exists():
                    PatientLab.objects.create(
                        **base_data,
                        lab_title=f'Lab - {instance.visit_title}'
                    )

            elif option.name == OPTION_REPORT:
                if not DentistReport.objects.filter(visit=instance).exists():
                    DentistReport.objects.create(
                        **base_data,
                        report_title=f'Report - {instance.visit_title}'
                    )

            elif option.name == OPTION_REFERRAL:
                if not PatientReferral.objects.filter(visit=instance).exists():
                    PatientReferral.objects.create(
                        **base_data,
                        referral_title=f'Referral - {instance.visit_title}'
                    )

            elif option.name == OPTION_TREATMENT:
                if not PatientTreatment.objects.filter(visit=instance).exists():
                    PatientTreatment.objects.create(
                        **base_data,
                        treatment_title=f'Treatment - {instance.visit_title}'
                    )


# ----------------------------- Manage patient bill -----------------------

@receiver(post_save, sender=PatientVisit)
def prepare_visit_bill(sender, instance, created, **kwargs):
    """ Create/update patient bill with total visit charges. """

    if instance.visit_status == 'Completed':
        total_charge = sum(service.price for service in instance.services.all())

        try:
            visit_bill = PatientBill.objects.get(visit=instance)

            visit_bill.total_charge = total_charge
            visit_bill.updated = timezone.now()
            visit_bill.save()
        except PatientBill.DoesNotExist:
            PatientBill.objects.create(
                patient=instance.patient,
                visit=instance,
                is_paid=False,
                total_charge=total_charge,
                bill_title=f'Bill - {instance.visit_title}'
            )

# Scrolling message for bill is ready
@receiver(post_save, sender=PatientVisit)
def bill_ready_message(sender, instance, created, **kwargs):
    """ Message from PatientVisit when status is completed """

    if instance.tracker.has_changed('visit_status') and instance.visit_status == 'Completed':
        message_text = ''

        try:
            bill_instance = instance.patientbill_visit
        except PatientBill.DoesNotExist:
            bill_instance = None

        PatientMessage.objects.create(
            visit=instance,
            bill=bill_instance,
            message=message_text
        )


# -------------------------- Treatment room signals ----------------------

# Set treatment room to occupied
@receiver(post_save, sender=PatientVisit)
def occupied_treatment_room(sender, instance, created, **kwargs):
    if instance.tracker.has_changed('visit_status') and instance.visit_status == 'Checked In':

        try:
            treatment_room = instance.treatmentroom_visit
        except TreatmentRoom.DoesNotExist:
            treatment_room = None

        TreatmentRoom.objects.filter(id=treatment_room.id).update(
            is_occupied = True
        )
        logger.info(f'Treatment Room {treatment_room.room_name} is to occupied.')


# Set treatment room to unoccupied
@receiver(post_save, sender=PatientVisit)
def release_treatment_room(sender, instance, created, **kwargs):
    if instance.tracker.has_changed('visit_status') and instance.visit_status == 'Closed':

        try:
            treatment_room = instance.treatmentroom_visit
        except TreatmentRoom.DoesNotExist:
            treatment_room = None

        TreatmentRoom.objects.filter(id=treatment_room.id).update(
            is_occupied = False
        )
        logger.info(f'Treatment Room {treatment_room.room_name} released after closed visit.')


# ------------ Update models with foreginkey relationships ---------------

# Update patient visit
@receiver(post_save, sender=PatientAppointment)
def update_visit_with_appointment(sender, instance, **kwargs):
    """ Update Patient visit branch, dentist, insurance with Patient appointment updates """

    PatientVisit.objects.filter(
        visit_title=instance.appointment_title
    ).update(
        visit_title=f'{instance.appointment_title}',
        dentist=instance.dentist,
        branch=instance.branch,
        insurance=instance.insurance
    )

# Update models related to PatientVisit
@receiver(post_save, sender=PatientVisit)
def updated_visit_related_models(sender, instance, **kwargs):
    """ Update PatientLab PatientReferral PatientTreatment when PatientVisit changes """

    PatientLab.objects.filter(
        visit=instance
    ).update(
        dentist=instance.dentist,
        branch=instance.branch,
        insurance=instance.insurance,
        appointment=instance.appointment,
        visit=instance
    )

    PatientReferral.objects.filter(
        visit=instance
    ).update(
        dentist=instance.dentist,
        branch=instance.branch,
        insurance=instance.insurance,
        appointment=instance.appointment,
        visit=instance
    )

    PatientTreatment.objects.filter(
        visit=instance
    ).update(
        dentist=instance.dentist,
        branch=instance.branch,
        insurance=instance.insurance,
        appointment=instance.appointment,
        visit=instance
    )


# ---------------------------- Messages -----------------------------------
# # New appointment message
# @receiver(post_save, sender=PatientAppointment)
# def new_appointment_message(sender, instance, created, **kwargs):
#     if created:
#         message_text = (f'Patient Appointment Message:- ',
#                         f'Appointment {instance.appointment_title} created for {instance.patient.full_name}',
#                         f'on {instance.appointment_date} at {instance.appointment_time}.')
#         PatientMessage.objects.create(message=message_text, appointment=instance)
#
#
# # Deactivate message
# @receiver(post_delete, sender=PatientAppointment)
# def deactivate_appointment_message(sender, instance, **kwargs):
#     try:
#         appointment_message = PatientMessage.objects.get(appointment=instance, is_active=True)
#         appointment_message.is_active = False
#         appointment_message.save()
#     except PatientMessage.DoesNotExist:
#         pass

# # New visit message
# @receiver(post_save, sender=PatientVisit)
# def new_visit_message(sender, instance, created, **kwargs):
#     if created:
#         message_text = (f'Patient Visit Message:- ',
#                         f'{instance.visit_title} created for {instance.patient}',
#                         f'on {instance.visit_date} at {instance.visit_time}.')
#         PatientMessage.objects.create(visit=instance, message=message_text)
