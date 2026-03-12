import logging
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import group_required
from mimascompany.models.employee_model import Employee
from patients.models.patients_model import Patient
from patients.forms.patient_form import PatientForm, PatientReadOnlyForm


logger = logging.getLogger(__name__)


# Create patient
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def create_patient(request):

    if request.method == 'POST':
        form = PatientForm(request.POST)

        if form.is_valid():
            new_patient = form.save(commit=False)
            new_patient.save()
            messages.success(request, f'New patient {new_patient.full_name} created.')
            logger.info(f'New patient {new_patient.full_name} created by {request.user}.')
            return redirect('patients:listpatients')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Patient Form Error:- {field} - {error}')
                    logger.info(f'Patient Form Error:- {field} - {error}')
    else:
        form = PatientForm()
    return render(request, 'patients/create_patient.html', {'h_form': form})


# Edit patient
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def edit_patient(request, pat_id):

    patient = Patient.objects.get(pk=pat_id)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)

        if form.is_valid():
            current_user = Employee.objects.get(user=request.user)
            edited_patient = form.save(commit=False)
            edited_patient.updated_by = current_user
            edited_patient.save()
            messages.success(request, f'Information for {edited_patient.full_name} updated.')
            logger.info(f'Patient {edited_patient.full_name} updated by {request.user}')
            return redirect('patients:listpatients')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Patient Form Error:- {field} - {error}')
                    logger.info(f'Patient Form Error:- {field} - {error}')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/create_patient.html', {'h_form': form})


# List patients
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def list_patients(request):

    query = request.GET.get('item_name')
    allpatients = Patient.objects.all().order_by('created')

    # Patient search
    if query:
        allpatients = allpatients.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(primary_dentist__employee__last_name__icontains=query) |
            Q(primary_dentist__employee__first_name__icontains=query)
        ).distinct()
    else:
        allpatients = Patient.objects.all().order_by('created')

    # Add pagination
    paginator = Paginator(allpatients, per_page=10)
    page_number = request.GET.get('page')
    page_patients = paginator.get_page(page_number)

    context = {
        'h_patients': allpatients,
        'page_patients': page_patients,
        'h_patientscount': allpatients.count()
    }
    return render(request, 'patients/list_patients.html', context)


# View patient
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def view_patient(request, pat_id):

    patient = get_object_or_404(Patient, pk=pat_id)
    form = PatientReadOnlyForm(instance=patient)

    for field in form.fields.values():
        field.disabled = True

    context = {
        'h_form': form,
        'h_patient': patient
    }
    return render(request, 'patients/view_patient.html', context)


# Delete patient
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def delete_patient(request, pat_id):

    patient = Patient.objects.get(pk=pat_id)
    if request.method == 'POST':
        logger.info(f'Patient {patient.full_name} delete requested by {request.user}!')
        patient.delete()
        messages.success(request, 'Patient deleted')
        logger.info('Patient deleted')
    return redirect('patients:listpatients')
