from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from accounts.decorators import group_required
from mimascompany.models import Dentist, Employee
from patients.models import (
    Patient,
    PatientLab,
    PatientVisit,
    PatientReferral,
    PatientTreatment,
    PatientAppointment
)


# Dentist dashboard
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators'])
def dentist_dashboard(request):

    try:
        employee = request.user.employee_accountuser
    except Employee.DoesNotExist:
        return None

    dentist = get_object_or_404(Dentist, employee=employee)

    patients = Patient.objects.filter(primary_dentist=dentist).count()
    next_visit = PatientVisit.objects.filter(
        dentist=dentist
    ).order_by(
        'visit_date', 'visit_time'
    ).first()
    next_appointment = PatientAppointment.objects.filter(
        dentist=dentist
    ).order_by(
        'appointment_date', 'appointment_time'
    ).first()

    context = {
        'h_dentist': dentist,
        'h_mypatients': patients,
        'h_nextvisit': next_visit,
        'h_nextappointment': next_appointment
    }
    return render(request, 'dentists/dentist_dashboard.html', context)
