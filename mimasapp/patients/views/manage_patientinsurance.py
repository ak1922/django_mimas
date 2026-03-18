from django.db.models import Q
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from mimascompany.models import Employee
from accounts.decorators import group_required
from patients.forms import PatientInsuranceForm
from patients.models import Patient, PatientInsurance


# Create insurance
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators', 'Employees'])
def create_insurance(request):

    next_url = request.GET.get('next', reverse('patients:listinsurance'))

    if request.method == 'POST':
        form = PatientInsuranceForm(request.POST)

        if form.is_valid():
            new_insurance = form.save()
            messages.success(request, f'Insurance information created for {new_insurance.patient.full_name}')
            return redirect(next_url)
        else:
            messages.error(request, 'Issues creating new insurance for patient.')

    else:
        form = PatientInsuranceForm()
    return render(request, 'patients/create_insurance.html', {'h_form': form})


# Add insurance from patients
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators', 'Employees'])
def create_patient_insurance_patient(request, pat_id=None):

    next_url = request.GET.get('next', reverse('patients:listinsurance'))

    patient_insurance = None
    if pat_id:
        requesting_patient = get_object_or_404(Patient, pk=pat_id)

        try:
            patient_insurance = requesting_patient.patientinsurance_patient
        except PatientInsurance.DoesNotExist:
            patient_insurance = PatientInsurance(patient=requesting_patient)

    if request.method == 'POST':
        form = PatientInsuranceForm(request.POST, instance=patient_insurance)

        if form.is_valid():
            requesting_patient = form.save()
            messages.success(request, f'Patient information for {requesting_patient.patient.full_name} updated.')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid form.')

    else:
        form = PatientInsuranceForm(instance=patient_insurance)
    return render(request, 'patients/create_insurance.html', {'h_form': form})


# Edit insurance
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators', 'Employees'])
def edit_insurance(request, ins_id):

    next_url = request.GET.get('next', reverse('patients:listinsurance'))

    insurance = PatientInsurance.objects.get(pk=ins_id)

    if request.method == 'POST':
        form = PatientInsuranceForm(request.POST, instance=insurance)

        if form.is_valid():
            current_user = Employee.objects.get(user=request.user)
            edited_insurance = form.save()
            edited_insurance.updated_by = current_user
            edited_insurance.save()
            messages.success(request, f'Insurance information updated for {edited_insurance.patient.full_name}')
            return redirect(next_url)
        else:
            messages.error(request, 'Issues with patient insurance information update.')

    else:
        form = PatientInsuranceForm(instance=insurance)
    return render(request, 'patients/create_insurance.html', {'h_form': form})


# List patient insurance
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators', 'Employees'])
def list_insurance(request):

    query = request.GET.get('item_name')
    patientscount = Patient.objects.all().count()
    allinsurance = PatientInsurance.objects.all().order_by('created')

    # Search
    if query:
        allinsurance = allinsurance.filter(
            Q(company__icontains=query) |
            Q(group_name__icontains=query)
        ).distinct()
    else:
        allinsurance = PatientInsurance.objects.all().order_by('created')

    # Pagination
    paginator = Paginator(allinsurance, per_page=10)
    page_number = request.GET.get('page')
    page_allinsurance = paginator.get_page(page_number)

    context = {
        'h_query': query,
        'h_patientscount': patientscount,
        'page_allinsurance': page_allinsurance,
        'h_insurancecount': allinsurance.count(),
    }
    return render(request, 'patients/list_insurance.html', context)


# Delete insurance
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators', 'Employees'])
def delete_insurance(request, ins_id):

    insurance = PatientInsurance.objects.get(pk=ins_id)
    if request.method == 'POST':
        insurance.delete()
        messages.success(request, 'Insurance information deleted.')
    return redirect('patients:listinsurance')
