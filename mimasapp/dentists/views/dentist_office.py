from datetime import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from accounts.decorators import group_required
from patients.models.patients_model import Patient
from patients.models.patientvisit_models import PatientVisit
from patients.models.patientappointment_model import PatientAppointment


# Dentist office
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators', 'Employees'])
def dentist_office(request):

    patientstotal = Patient.objects.all().count()
    visitstotal = PatientVisit.objects.all().count()
    appointmentstotal = PatientAppointment.objects.all().count()

    context = {
        'h_visitstotal': visitstotal,
        'h_patientstotal': patientstotal,
        'h_appointmentstotal': appointmentstotal
    }
    return render(request, 'dentists/dentist_office.html', context)
