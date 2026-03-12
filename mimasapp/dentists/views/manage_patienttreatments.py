import logging
from django.db.models import Q
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from mimascompany.models.employee_model import Employee
from accounts.decorators import group_required
from dentists.forms.patienttreatment_forms import PatientTreatmentForm
from dentists.forms.archived_forms import ArchivedPatientTreatmentForm
from patients.models.patients_model import Patient
from patients.models.patientvisit_models import PatientVisit
from patients.models.patienttreatment_model import PatientTreatment
from patients.models.arcivedtreatment_model import ArchivedPatientTreatment


logger = logging.getLogger(__name__)


# Create treatment
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def create_treatment(request):

    next_url = request.GET.get('next', reverse('dentists:listalltreatments'))
    if request.method == 'POST':
        form = PatientTreatmentForm(request.POST)

        if not request.user.user_type == 'Dentists':
            for field in form.fields.values():
                field.disabled = True
        else:
            if form.is_valid():
                treatment = form.save()
                messages.success(request, f'New treatment {treatment.treatment_title} created for visit {treatment.visit}.')
                logger.info(f'New treatment {treatment.treatment_title} created for visit {treatment.visit} by {request.user}.')
                return redirect(next_url)
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'Patient Treatment Form Error:- {field} - {error}')
                        logger.info(f'Patient Treatment Form Error:- {field} - {error}')
    else:
        form = PatientTreatmentForm()
        if not request.user.user_type == 'Dentists':
            for field in form.fields.values():
                field.disabled = True

    context = {
        'h_form': form,
        'h_exisitng_treatment': None
    }
    return render(request, 'dentists/create_treatment.html', context)


# Create treatment from visit
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def create_treatment_patient_visit(request, vis_id=None):

    visit = get_object_or_404(PatientVisit, pk=vis_id)

    if request.method == 'POST':
        form = PatientTreatmentForm(request.POST)

        if form.is_valid():
            treatment = form.save(commit=False)
            treatment.patient = visit.patient
            treatment.dentist = visit.dentist or None
            treatment.branch = visit.branch or None
            treatment.insurance = visit.insurance or None
            treatment.appointment = visit.appointment or None
            treatment.visit = visit
            treatment.save()
            messages.success(request, f'New patient treatment {treatment.treatment_title} created for visit {treatment.visit}.')
            logger.info(f'New patient treatment {treatment.treatment_title} created for visit {treatment.visit} by {request.user}.')
            return redirect('patients:listallpatientvisits')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Patient Treatment Form Error:- {field} - {error}')
                    logger.info(f'Patient Treatment Form Error:- {field} - {error}')
    else:
        form = PatientTreatmentForm(initial={
            'patient': visit.patient,
            'dentist': visit.dentist,
            'branch': visit.branch,
            'insurance': visit.insurance,
            'appointment': visit.appointment,
            'visit': visit
        })

    context = {
        'h_form': form,
        'h_exisitng_treatment': None
    }
    return render(request, 'dentists/create_treatment.html', context)


# Edit treatment
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def edit_treatment(request, tre_id):

    treatment = PatientTreatment.objects.get(pk=tre_id)

    if request.method == 'POST':
        form = PatientTreatmentForm(request.POST, instance=treatment)

        if form.is_valid():
            current_user = Employee.objects.get(user=request.user)
            edited_treatment = form.save(commit=False)
            edited_treatment.updated_by = current_user
            edited_treatment.save()
            messages.success(request, f'{edited_treatment.treatment_title} information updated.')
            logger.info(f'{edited_treatment.treatment_title} information updated by {request.user}.')
            return redirect('dentists:listalltreatments')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Patient Treatment Form Error:- {field} - {error}')
                    logger.info(f'Patient Treatment Form Error:- {field} - {error}')
    else:
        form = PatientTreatmentForm(instance=treatment)

    context = {
        'h_form': form,
        'h_exisitng_treatment': None
    }
    return render(request, 'dentists/create_treatment.html', context)


# View treatment
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def view_treatment(request, tre_id):

    treatment = PatientTreatment.objects.get(pk=tre_id)
    form = PatientTreatmentForm(instance=treatment)

    for field in form.fields.values():
     field.disabled = True

    context = {
        'h_form': form,
        'h_exisitng_treatment': treatment
    }
    return render(request, 'dentists/create_treatment.html', context)


# List patient treatments
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def list_all_treatments(request):

    treatments = PatientTreatment.objects.all().order_by('-created')
    query = request.GET.get('item_name')

    if query:
        treatments = treatments.filter(
            Q(treatment_title__icontains=query) |
            Q(patient__first_name=query) |
            Q(patient__last_name=query) |
            Q(dentist__employee__first_name__icontains=query) |
            Q(dentist__employee__last_name__icontains=query)
        ).distinct()
    else:
        treatments = PatientTreatment.objects.all().order_by('-created')

    paginator = Paginator(treatments, per_page=10)
    page_number = request.GET.get('page')
    page_treatments = paginator.get_page(page_number)

    context = {
        'page_treatments': page_treatments,
        'h_treatmentscount': treatments.count()
    }
    return render(request, 'dentists/list_treatments.html', context)


# List patient treatment
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def list_patient_treatments(request, pat_id):

    patient = get_object_or_404(Patient, pk=pat_id)
    alltreatments = PatientTreatment.objects.filter(patient=patient)

    context = {
        'h_patient': patient,
        'page_treatments': alltreatments
    }
    return render(request, 'dentists/list_onepatient_treats.html', context)


# Delete treatment
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def delete_treatment(request, tre_id):

    treatment = PatientTreatment.objects.get(pk=tre_id)

    if request.method == 'POST':
        logger.info(f'{treatment.treatment_title} delete requested by {request.user}.')
        treatment.delete()
        messages.success(request, 'Treatment deleted.')
        logger.info(f'Treatment deleted.')
    return redirect('dentists:listalltreatments')



# ------------------------ Archived Treatments ---------------------------

# View archived treatment
@login_required
def view_archived_treatment(request, tre_id):

    archived_treatment = ArchivedPatientTreatment.objects.get(pk=tre_id)
    form = ArchivedPatientTreatmentForm(instance=archived_treatment)

    for field in form.fields.values():
        field.disabled = True

    context = {
        'h_form': form,
        'h_archivedtreatment': archived_treatment
    }
    return render(request, 'dentists/view_archivedtreatment.html', context)


# List archived treatments
@login_required
def list_all_archived_treatments(request):

    archivedtreatments = ArchivedPatientTreatment.objects.all().order_by('archived')
    query = request.GET.get('item_name')

    if query:
        archivedtreatments = archivedtreatments.filter(
            Q(treatment_title__icontains=query) |
            Q(patient__first_name=query) |
            Q(patient__last_name=query)
        ).distinct()
    else:
        archivedtreatments = ArchivedPatientTreatment.objects.all().order_by('archived')

    paginator = Paginator(archivedtreatments, per_page=10)
    page_number = request.GET.get('page')
    page_archivedtreatments = paginator.get_page(page_number)

    context = {
        'h_archivedcount': archivedtreatments.count(),
        'page_archivedtreatments': page_archivedtreatments,
    }
    return render(request, 'dentists/list_archivedtreatments.html', context)
