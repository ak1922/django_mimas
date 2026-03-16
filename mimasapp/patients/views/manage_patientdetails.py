import logging
from django.db.models import Q
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import group_required
from mimascompany.models.employee_model import Employee
from patients.models.patients_model import Patient
from patients.models.patientdetails_model import PatientDetail
from patients.forms.patientdetail_form import PatientDetailForm, PatientDetailReadOnlyForm


logger = logging.getLogger(__name__)


# Create detail
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def create_patient_detail(request):

    next_url = request.GET.get('next', reverse('patients:listpatientdetails'))
    if request.method == 'POST':
        form = PatientDetailForm(request.POST)

        if form.is_valid():
            new_detail = form.save()
            messages.success(request, f'New details for Patient {new_detail.patient} created.')
            logger.info(f'New details for Patient {new_detail.patient} created by {request.user}.')
            return redirect(next_url)
        else:
            messages.error(request, 'Issues creating new detail')

    else:
        form = PatientDetailForm()
    return render(request, 'patients/create_patientdetail.html', {'h_form': form})


# Add details from patient
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def create_patient_detail_patient(request, pat_id=None):

    next_url = request.GET.get('next', reverse('patients:listpatientdetails'))
    patient_detail = None
    if pat_id:
        requesting_patient = get_object_or_404(Patient, pk=pat_id)

        try:
            patient_detail = requesting_patient.patientdetail_patient
        except PatientDetail.DoesNotExist:
            patient_detail = PatientDetail(patient=requesting_patient)

    if request.method == 'POST':
        form = PatientDetailForm(request.POST, instance=patient_detail)

        if form.is_valid():
            new_details = form.save()
            messages.success(request, f'New details for Patient {new_details.patient} created.')
            logger.info(f'New details for Patient {new_details.patient} created by {request.user}.')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid form submitted!')

    else:
        form = PatientDetailForm(instance=patient_detail)

    context = {
        'h_form': form,
        'h_patientdetail': patient_detail
    }
    return render(request, 'patients/create_patientdetail.html', context)


# Edit detail
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def edit_patient_detail(request, det_id):

    next_url = request.GET.get('next', reverse('patients:listpatientdetails'))
    detail = PatientDetail.objects.get(pk=det_id)

    if request.method == 'POST':
        form = PatientDetailForm(request.POST, instance=detail)

        if form.is_valid():
            current_user = Employee.objects.get(user=request.user)
            edited_detail = form.save(commit=False)
            edited_detail.updated_by = current_user
            edited_detail.save()
            form.save_m2m()
            messages.success(request, f'Patient details for {edited_detail.patient} updated')
            logger.info(f'Patient details for {edited_detail.patient} updated by {request.user}')
            return redirect(next_url)
        else:
            messages.error(request, 'Issues encounted with detail update.')

    else:
        form = PatientDetailForm(instance=detail)
    return render(request, 'patients/create_patientdetail.html', {'h_form': form})


# List patient details
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def list_patient_details(request):

    query = request.GET.get('page_item')
    allpatients = Patient.objects.all().count()
    allpatientdetails = PatientDetail.objects.all().order_by('created')

    if query:
        allpatientdetails = allpatientdetails.filter(
            Q(patient__icontains=query)
        ).distinct()
    else:
        allpatientdetails = PatientDetail.objects.all().order_by('created')

    paginator = Paginator(allpatientdetails, per_page=10)
    page_number = request.GET.get('page')
    page_patientdetails = paginator.get_page(page_number)

    context = {
        'h_query': query,
        'h_allpatients': allpatients,
        'page_patientdetails': page_patientdetails,
        'h_detailstotal': allpatientdetails.count()
    }
    return render(request, 'patients/list_patientdetails.html', context)


# Patient details read only
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def view_patient_detail(request, det_id):

    detail = PatientDetail.objects.get(pk=det_id)
    form = PatientDetailReadOnlyForm(instance=detail)

    for field in form.fields.values():
        field.disabled = True

    context = {
        'h_form': form,
        'h_detail': detail
    }
    return render(request, 'patients/view_patientdetails.html', context)


# Delete detail
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def delete_patient_detail(request, det_id):

    detail = PatientDetail.objects.get(pk=det_id)
    if request.method == 'POST':
        detail.delete()
        messages.success(request, 'Patient detail deleted.')
    return redirect('patients:listpatientdetails')
