from datetime import date
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from patients.models import (
    Patient,
    PatientVisit,
    PatientAppointment,
    ArchivedPatientLab,
    ArchivedPatientVisit,
    ArchivedPatientReferral,
    ArchivedPatientTreatment,
    AppointmentStatus
)


@login_required
def patient_dashboard(request):

    today = date.today()
    patient = Patient.objects.get(patient=request.user)

    completedvisits = ArchivedPatientVisit.objects.filter(patient=patient).count()
    completedlabs = ArchivedPatientLab.objects.filter(patient=patient).count()
    completedreferrals = ArchivedPatientReferral.objects.filter(patient=patient).count()
    completedtreatments = ArchivedPatientTreatment.objects.filter(patient=patient).count()

    confirmed = PatientAppointment.objects.filter(
        patient=patient,
        status=AppointmentStatus.CONFIRMED
    ).count()
    unconfirmed = PatientAppointment.objects.filter(
        patient=patient,
        status=AppointmentStatus.SCHEDULED
    ).count()
    scheduledvisits = PatientVisit.objects.filter(
        patient=patient,
        visit_status__exact='Created'
    ).count()
    noshowvisits = PatientVisit.objects.filter(
        patient=patient,
        visit_status__exact='No Show'
    ).count()

    next_appointment = PatientAppointment.objects.filter(
        patient=patient,
    ).order_by('appointment_date').first()

    days_left = None
    if next_appointment:
        dalta = next_appointment.appointment_date - today
        days_left = dalta.days

    context = {
        'h_patient': patient,
        'h_daysleft': days_left,
        'h_unconfirmed': unconfirmed,
        'h_confirmed': confirmed,
        'h_scheduledvisits': scheduledvisits,
        'h_completedvisits': completedvisits,
        'h_noshowvisits': noshowvisits,
        'h_completedlabs': completedlabs,
        'h_nextappointment:': next_appointment,
        'h_completedreferrals': completedreferrals,
        'h_completedtreatments': completedtreatments
    }
    return render(request, 'patients/patient_dashboard.html', context)


# Unconfirmed appointments
@login_required
def patient_unconfirmed_appointments(request, pat_id):

    patient = get_object_or_404(Patient, pk=pat_id)
    unconfirmed = PatientAppointment.objects.filter(
        patient=patient,
        status__exact=AppointmentStatus.SCHEDULED
    )

    context = {
        'h_patient': patient,
        'h_unconfirmed': unconfirmed
    }
    return render(request, 'patients/unconfirmed_appointments.html', context)


# Confirmed appointments
@login_required
def patient_confirmed_appointment(request, pat_id):

    patient = get_object_or_404(Patient, pk=pat_id)
    confirmed = PatientAppointment.objects.filter(
        patient=patient,
        status__exact=AppointmentStatus.CONFIRMED
    )

    context = {
        'h_patient': patient,
        'h_confirmed': confirmed
    }
    return render(request, 'patients/confirmed_appointments.html', context)


# Scheduled visits
@login_required
def patient_scheduled_visits(request, pat_id):

    patient = get_object_or_404(Patient, pk=pat_id)
    visits = PatientVisit.objects.filter(
        patient=patient,
        visit_status='Created'
    )

    context = {
        'h_patient': patient,
        'h_scheduledvisits': visits
    }
    return render(request, 'patients/scheduled_visits.html', context)


# Closed visits
@login_required
def patient_completed_visits(request, pat_id):

    patient = get_object_or_404(Patient, pk=pat_id)
    visits = ArchivedPatientVisit.objects.filter(patient=patient)

    context = {
        'h_patient': patient,
        'h_completedvisits': visits
    }
    return render(request, 'patients/completed_visits.html', context)


# Completed treatments
@login_required
def patient_completed_treatments(request, pat_id):

    patient = get_object_or_404(Patient, pk=pat_id)
    treatments = ArchivedPatientTreatment.objects.filter(patient=patient)

    context = {
        'h_patient': patient,
        'h_treatments': treatments
    }
    return render(request, 'patients/completed_treatments.html', context)


# Completed labs
@login_required
def patient_completed_labs(request, pat_id):

    patient = get_object_or_404(Patient, pk=pat_id)
    labs = ArchivedPatientLab.objects.filter(patient=patient)

    context = {
        'h_labs': labs,
        'h_patient': patient
    }
    return render(request, 'patients/completed_labs.html', context)


# Completed referrals
@login_required
def patient_completed_referrals(request, pat_id):

    patient = get_object_or_404(Patient, pk=pat_id)
    referrals = ArchivedPatientReferral.objects.filter(patient=patient)

    context = {
        'h_patient': patient,
        'h_referrals': referrals
    }
    return render(request, 'patients/completed_referrals.html', context)
