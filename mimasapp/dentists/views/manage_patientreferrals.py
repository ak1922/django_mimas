import logging
from django.db.models import Q
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import group_required
from mimascompany.models.employee_model import Employee
from dentists.forms.patientreferral_forms import PatientReferralForm
from dentists.forms.archived_forms import ArchivedPatientReferralForm
from patients.models.patients_model import Patient
from patients.models.patientvisit_models import PatientVisit
from patients.models.patientreferral_model import PatientReferral
from patients.models.archivedreferral_model import ArchivedPatientReferral


logger = logging.getLogger(__name__)


# Create referral
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators', 'Employees'])
def create_referral(request):

    next_url = request.GET.get('next', reverse('dentists:listallpatientreferrals'))
    if request.method == 'POST':
        form = PatientReferralForm(request.POST)

        if not request.user.user_type == 'Dentists':
            for field in form.fields.values():
                field.disabled = True
        else:
            if form.is_valid():
                new_referral = form.save()
                messages.success(request, f'New referral {new_referral.referral_title} created for {new_referral.patient}')
                logger.info(f'New referral {new_referral.referral_title} created for {new_referral.patient}')
                return redirect(next_url)
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'Patient Referral Form Error:- {field} - {error}')
                        logger.info(f'Patient Referral Form Error:- {field} - {error}')
    else:
        form = PatientReferralForm()
        if not request.user.user_type == 'Dentists':
            for field in form.fields.values():
                field.disabled = True

    context = {
        'h_form': form,
        'h_existing_referral': None
    }
    return render(request, 'dentists/create_referral.html', context)


# Create referral from visits
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators', 'Employees'])
def create_referral_patient_visit(request, vis_id=None):

    visit = get_object_or_404(PatientVisit, pk=vis_id)

    if request.method == 'POST':
        form = PatientReferralForm(request.POST)

        if form.is_valid():
            new_referral = form.save(commit=False)
            new_referral.patient = visit.patient
            new_referral.dentist = visit.dentist
            new_referral.branch = visit.branch
            new_referral.insurance = visit.insurance
            new_referral.appointment = visit.appointment
            new_referral.visit = visit
            new_referral.save()
            messages.success(request, f'New Referral {new_referral.referral_title} created for Visit {new_referral.visit}.')
            logger.info(f'New Referral {new_referral.referral_title} created for Visit {new_referral.visit} by {request.user}.')
            return redirect('patients:listallpatientvisits')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Patient Referral Form Error:- {field} - {error}')
                    logger.info(f'Patient Referral Form Error:- {field} - {error}')
    else:
        form = PatientReferralForm(initial={
            'patient': visit.patient,
            'dentist': visit.dentist,
            'branch': visit.branch,
            'insurance': visit.insurance,
            'appointment': visit.appointment,
            'visit': visit
        })

    context = {
        'h_form': form,
        'h_existing_referral': None
    }
    return render(request, 'dentists/create_referral.html', context)


# Edit referral
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators', 'Employees'])
def edit_referral(request, ref_id):
    """ Edit patient referral """

    next_url = request.GET.get('next', reverse('dentists:listallpatientreferrals'))
    referral = PatientReferral.objects.get(pk=ref_id)

    if request.method == 'POST':
        form = PatientReferralForm(request.POST, instance=referral)

        if form.is_valid():
            current_user = Employee.objects.get(user=request.user)
            edited_referral = form.save(commit=False)
            edited_referral.updated_by = current_user
            edited_referral.save()
            messages.success(request, f'{edited_referral.referral_title}, updated for patient {edited_referral.patient}')
            logger.info(f'{edited_referral.referral_title}, updated for patient {edited_referral.patient} by {request.user}.')
            return redirect(next_url)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Patient Referral Form Error:- {field} - {error}')
                    logger.info(f'Patient Referral Form Error:- {field} - {error}')
    else:
        form = PatientReferralForm(instance=referral)

    context = {
        'h_form': form,
        'h_existing_referral': None
    }
    return render(request, 'dentists/create_referral.html', context)


# View referral
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators', 'Employees'])
def view_referral(request, ref_id):
    """ Read only view for patient referral """

    referral = PatientReferral.objects.get(pk=ref_id)
    form = PatientReferralForm(instance=referral)

    for field in form.fields.values():
        field.disabled = True

    context = {
        'h_form': form,
        'h_existing_referral': referral
    }
    return render(request, 'dentists/create_referral.html', context)


# List referrals
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators', 'Employees'])
def list_all_patient_referrals(request):

    query = request.GET.get('page')
    allreferrals = PatientReferral.objects.all().order_by('-created')

    # Serarch
    if query:
        allreferrals = allreferrals.filter(
            Q(referral_title__icontains=query) |
            Q(patient__first_name=query) |
            Q(patient__last_name=query)
        ).distinct()
    else:
        allreferrals = PatientReferral.objects.all().order_by('-created')

    # Pagination
    paginator = Paginator(allreferrals, per_page=10)
    page_number = request.GET.get('page')
    page_allreferrals = paginator.get_page(page_number)

    context = {
        'page_allreferrals': page_allreferrals,
        'h_referralscount': allreferrals.count(),
    }
    return render(request, 'dentists/list_referrals.html', context)


# List patient referrals
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators', 'Employees'])
def list_patient_referrals(request, pat_id):
    """ List referrals for a patient """

    query = request.GET.get('item_name')
    patient = get_object_or_404(Patient, pk=pat_id)
    patient_referrals = PatientReferral.objects.filter(patient=patient).order_by('-created')

    if query:
        patient_referrals = patient_referrals.filter(
            Q(referral_title__icontains=query)
        ).distinct()
    else:
        patient_referrals = PatientReferral.objects.filter(patient=patient).order_by('-created')

    context = {
        'h_patient': patient,
        'page_allreferrals': patient_referrals,
        'h_referralscount': patient_referrals.count()
    }
    return render(request, 'dentists/list_onepatient_referrals.html', context)


# Delete referral
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators', 'Employees'])
def delete_referral(request, ref_id):

    referral = PatientReferral.objects.get(pk=ref_id)

    if request.method == 'POST':
        referral.delete()
        messages.success(request, 'Patient referral deleted.')
    return redirect('dentists:listallreferrals')


# ----------------------------- Archived Referrals -----------------------------

# View archived referral
@login_required
def view_archived_referral(request, ref_id):
    """ View archived patient referral """

    archived_referral = ArchivedPatientReferral.objects.get(pk=ref_id)
    form = ArchivedPatientReferralForm(instance=archived_referral)

    for field in form.fields.values():
        field.disabled = True

    context = {
        'h_form': form,
        'h_archivedreferral': archived_referral
    }
    return render(request, 'dentists/view_archivedreferral.html', context)


# List archived referrals
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators', 'Employees'])
def list_all_archived_referrals(request):
    """ List all archived patient referrals """

    allarchivedreferrals = ArchivedPatientReferral.objects.all().order_by('-archived_on')
    archivedcount = ArchivedPatientReferral.objects.all().count()
    query = request.GET.get('item_name')

    # Search
    if query:
        allarchivedreferrals = allarchivedreferrals.filter(
            Q(referral_title__icontains=query) |
            Q(patient__first_name=query) |
            Q(patient__last_name=query)
        ).distinct()
    else:
        allarchivedreferrals = ArchivedPatientReferral.objects.all().order_by('-archived_on')

    # Pagination
    paginator = Paginator(allarchivedreferrals, 10)
    page_number = request.GET.get('page')
    page_allarchivedreferrals = paginator.get_page(page_number)

    context = {
        'h_archivedcount': archivedcount,
        'page_allarchivedreferrals': page_allarchivedreferrals
    }
    return render(request, 'dentists/list_archivedreferrals.html', context)
