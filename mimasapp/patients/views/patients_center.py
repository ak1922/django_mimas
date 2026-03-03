from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from accounts.decorators import group_required
from patients.models.patients_model import Patient


# Patients center
@login_required
@group_required(allowed_groups=['Dentists', 'Employees', 'Administrators'])
def patientscenter(request):

    all_patients = Patient.objects.all().count()

    context = {
        'h_allpatients': all_patients,
    }
    return render(request, 'patients/patients_center.html', context)
