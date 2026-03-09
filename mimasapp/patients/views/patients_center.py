from typing import List, Union
from django.db.models import Max
from datetime import date
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from accounts.decorators import group_required
from patients.models.patients_model import Patient
from patients.models.patientmessage_model import PatientMessage
from patients.models.patientvisit_models import PatientVisit
from patients.models.patientappointment_model import PatientAppointment


# Patients center
@login_required
@group_required(allowed_groups=['Dentists', 'Employees', 'Administrators'])
def patientscenter(request):

    today = date.today()

    all_patients = Patient.objects.all().count()
    appointments_total = PatientAppointment.objects.all().count()
    visits_total = PatientVisit.objects.all().count()
    visit_today_count = PatientVisit.objects.filter(visit_date=today).count()

    # ---- Daily message ----
    daily_message = f"Today is {today.strftime('%A, %B %d, %Y')}"

    class DummyMessage:
        def __init__(self, message, msg_type='date'):
            self.message = message
            self.type = msg_type

    message_list : List[Union[DummyMessage, PatientMessage]] = [DummyMessage(daily_message)]
    visit_today_count_text = f'Number of Patient visits today...{visit_today_count}'
    visit_today_count_msg, created = PatientMessage.objects.get_or_create(
        message=visit_today_count_text,
        defaults={'created': today}
    )

    if not created:
        PatientMessage.objects.filter(
            message__startswith='Number of Patient visits today...'
        ).exclude(id=visit_today_count_msg.id).delete()
    message_list.append(visit_today_count_msg)

    # ---- Patient details messages ----
    details_message_text = 'Patient Details Message:- '
    number_without_details = Patient.patient_without_details.without_details().count()
    missing_details_message, _ = PatientMessage.objects.get_or_create(
        defaults={'is_active': True},
        message=f'{details_message_text} {number_without_details} patient/s without detail record/s.'
    )
    message_list.append(missing_details_message)

    without_detail = Patient.patient_without_details.without_details()
    for patient in without_detail:
        person_detail_message, _ = PatientMessage.objects.get_or_create(
            defaults={'is_active': True},
            message=f'{details_message_text} {patient.full_name} missing Patient Details.'
        )
        message_list.append(person_detail_message)

    # ---- Patient contact messages ----
    contact_message_text = 'Patient Contacts Message:- '
    number_without_contact = Patient.patient_without_contact.without_contact().count()
    missing_contact_message, _ = PatientMessage.objects.get_or_create(
        defaults={'is_active': True},
        message=f'{contact_message_text} {number_without_contact} patient/s without contact record/s.'
    )
    message_list.append(missing_contact_message)

    without_contact = Patient.patient_without_contact.without_contact()
    for patient in without_contact:
        person_contact_message, _ = PatientMessage.objects.get_or_create(
            defaults={'is_active': True},
            message=f'{contact_message_text} {patient.full_name} missing Patient Contact.'
        )
        message_list.append(person_contact_message)

    # ---- Patients insurance messages ----
    insurance_message_text = 'Patient Insurance Message:- '
    number_without_insurance = Patient.patient_without_insurance.without_insurance().count()
    missing_insuarnce_message, _ = PatientMessage.objects.get_or_create(
        defaults={'is_active': True},
        message=f'{insurance_message_text} {number_without_insurance} patient/s without insurance record/s.'
    )
    message_list.append(missing_insuarnce_message)

    without_insurance = Patient.patient_without_insurance.without_insurance()
    for patient in without_insurance:
        person_insurance_message, _ = PatientMessage.objects.get_or_create(
            defaults={'is_active': True},
            message=f'{insurance_message_text} {patient.full_name} missing Patient Insurance.'
        )
        message_list.append(person_insurance_message)

    # ---- Visit & Appointment messages ----
    appointment_message_ids = PatientMessage.objects.filter(
        is_active=True,
        visit__isnull=False
    ).values(
        'visit'
    ).annotate(max_id=Max('id')).values_list('max_id', flat=True)
    visit_message_ids = PatientMessage.objects.filter(
        is_active=True,
        visit__isnull=False
    ).values(
        'visit'
    ).annotate(max_id=Max('id')).values_list('max_id', flat=True)
    combo_message_ids = set(list(appointment_message_ids) + list(visit_message_ids))

    appoint_visit_msgs = PatientMessage.objects.filter(
        is_active=True,
        id__in=combo_message_ids
    ).order_by('created')[:10]
    message_list.extend(appoint_visit_msgs)

    context = {
        'h_allpatients': all_patients,
        'h_visitstotal': visits_total,
        'h_messages': message_list,
        'h_appointmentstotal': appointments_total
    }
    return render(request, 'patients/patients_center.html', context)
