import logging
from datetime import date
from django.urls import reverse
from django.db import transaction
from django.contrib import messages
from django.db.models import Sum, Q
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from patients.utils import perform_archiving
from accounts.decorators import group_required
from mimascompany.models import Employee, Department
from patients.forms import PatientVisitForm, ArchivedPatientVisitReadOnlyForm
from patients.models import (
    Patient,
    PatientVisit,
    PatientBill,
    PatientVisitTask,
    ArchivedPatientVisit,
    PatientMessage
)


logger = logging.getLogger(__name__)


# Create visit
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators', 'Employees'])
def create_patient_visit(request):

    next_url = request.GET.get('next', reverse('patients:listallpatientvisits'))

    if request.method == 'POST':
        form = PatientVisitForm(request.POST)
        if form.is_valid():

            task_owner = Employee.active_employees.get(user=request.user)

            try:
                with transaction.atomic():
                    new_visit = form.save(commit=False)
                    new_visit.save()
                    form.save_m2m()
                    logger.info(f'New patient visit {new_visit.visit_title} created by {task_owner}.')

                    # Create visit task
                    visit_task = PatientVisitTask.objects.create(
                        visit=new_visit,
                        assigned_to = task_owner,
                        task_title=f'Visit Task - {new_visit.visit_title}',
                    )
                    logger.info(f'New Visit Task created for {visit_task.assigned_to}')
                    messages.success(request, f'New visit {new_visit.visit_title} created for {new_visit.patient.full_name}')
                    return redirect(next_url)

            except Exception as e:
                messages.error(request, f'An error occurred: {e}')

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}:- {error}')
                    logger.error(f'{field}:- {error}')
    else:
        form = PatientVisitForm()

    # Setup for checkboxes
    departments = Department.objects.prefetch_related('service_department').all()

    context = {
        'h_form': form,
        'h_exists_visit': None,
        'h_departments': departments,
    }
    return render(request, 'patients/create_patientvisit.html', context)


# Edit visit
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators', 'Employees'])
def edit_patient_visit(request, vis_id):
    """ Manage visits """

    visit = get_object_or_404(PatientVisit, pk=vis_id)
    original_status = visit.visit_status
    has_unpaid_bill = PatientBill.objects.filter(id=visit.id, is_paid=False).exists()
    next_url = request.GET.get('next', reverse('patients:listallpatientvisits'))

    if request.method == 'POST':
            form = PatientVisitForm(request.POST, instance=visit)
            if form.is_valid():
                current_user = Employee.objects.get(user=request.user)
                edited_visit = form.save(commit=False)
                edited_visit.updated_by = current_user

                with transaction.atomic():
                    if edited_visit.visit_status == 'Closed' and original_status != 'Closed':
                        if has_unpaid_bill:
                            edited_visit.visit_status = 'Completed'
                            edited_visit.save()
                            form.save_m2m()
                            messages.error(request, 'Patient bill for visit is unpaid. Status set to Completed, not Closed.')
                            return redirect('patients:listpatientbills')
                        else:
                            edited_visit.save()
                            form.save_m2m()
                    else:
                        edited_visit.save()
                        form.save_m2m()
                        PatientMessage.objects.create(
                            visit=edited_visit,
                            message=f"Patient Visit Message:- {edited_visit.visit_title} for patient {edited_visit.patient.full_name} status updated."
                        )
                        messages.success(request, "Visit updated successfully.")
                        return redirect(next_url)

            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'Patient Visit Form Error:- {field}: {error}')
                        logger.error(f'Patient Visit Form Error:- {field}: {error}')

    else:
        form = PatientVisitForm(instance=visit)

    selected_service_ids = visit.services.values_list('id', flat=True)
    selected_dept_ids = visit.departments.values_list('department_id', flat=True)
    departments = Department.objects.prefetch_related('service_department').all()

    context = {
        'h_form': form,
        'h_departments': departments,
        'h_selecteddeptids': selected_dept_ids,
        'h_selectedserviceids': selected_service_ids
    }
    return render(request, 'patients/create_patientvisit.html', context)


# Patient visit read only
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators', 'Employees', 'Patients'])
def view_patient_visit(request, vis_id):

    visit = PatientVisit.objects.get(pk=vis_id)
    form = PatientVisitForm(instance=visit)

    for field in form.fields.values():
        field.disabled = True

    lab = None
    report = None
    referral = None
    treatment = None

    try:
        lab = visit.patientlab_visit.order_by('-id').first()
    except ObjectDoesNotExist:
        lab = None
    try:
        report = visit.dentistreport_visit.order_by('-id').first()
    except ObjectDoesNotExist:
        report = None
    try:
        referral = visit.patientreferral_visit.order_by('-id').first()
    except ObjectDoesNotExist:
        referral = None
    try:
        treatment = visit.patienttreatment_visit.order_by('-id').first()
    except ObjectDoesNotExist:
        treatment = None

    context = {
        'h_lab': lab,
        'h_form': form,
        'h_visit': visit,
        'h_report': report,
        'h_referral': referral,
        'h_treatment': treatment,
        'h_exists_visit': visit
    }
    return render(request, 'patients/create_patientvisit.html', context)


# View patient bill
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators', 'Employees'])
def view_visit_cost(request, vis_id):
    """ View dental services """

    visit = PatientVisit.objects.get(pk=vis_id)
    total_cost = visit.services.aggregate(total_sum=Sum('price'))['total_sum']

    context = {
        'h_visit': visit,
        'h_totalcost': total_cost
    }
    return render(request,'patients/visit_cost.html', context)


# List all visits
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators', 'Employees'])
def list_all_patient_visits(request):
    """ List visits for all patients """

    today = date.today()
    query = request.GET.get('item_name')
    allvisits = PatientVisit.objects.order_by('visit_date')

    if query:
        allvisits = allvisits.filter(
            Q(visit_title__icontains=query) |
            Q(patient__last_name__icontains=query) |
            Q(patient__first_name__icontains=query)
        ).distinct()
    else:
        allvisits = PatientVisit.objects.all().order_by('visit_date')

    paginator = Paginator(allvisits, per_page=10)
    page_number = request.GET.get('page')
    page_allvisits = paginator.get_page(page_number)

    context = {
        'h_today': today,
        'page_allvisits': page_allvisits,
        'h_visitstotal': allvisits.count(),
    }
    return render(request, 'patients/list_patientvisits.html', context)


# List patient visits
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators', 'Employees'])
def list_patient_visits(request, pat_id):
    """ List visits for one patient """

    query = request.GET.get('item_name')
    patient = get_object_or_404(Patient, pk=pat_id)
    patient_visits = PatientVisit.objects.filter(patient=patient).order_by('-updated')

    if query:
        patient_visits = patient_visits.filter(
            Q(visit_title__icontains=query) |
            Q(patient__last_name__icontains=query) |
            Q(patient__first_name__icontains=query)
        ).distinct()
    else:
        patient_visits = PatientVisit.objects.filter(patient=patient).order_by('-updated')

    paginator = Paginator(patient_visits, per_page=10)
    page_number = request.GET.get('page')
    page_patientvisits = paginator.get_page(page_number)

    context = {
        'h_patient': patient,
        'page_patientvisits': page_patientvisits,
        'h_visitstotal': patient_visits.count()
    }
    return render(request, 'patients/listvisits_onepatient.html', context)


# Delete visit
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators', 'Employees'])
def delete_patient_visit(request, vis_id):

    visit = PatientVisit.objects.get(pk=vis_id)

    if request.method == 'POST':
        visit.delete()
        messages.success(request, 'Patient visit deleted!')
    return redirect('patients:listallpatientvisits')


# -------------------------- ARCHIVED VISITS ----------------------------------

# Archive visit
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators', 'Employees'])
def archive_patient_visit(request, vis_id):

    visit = get_object_or_404(PatientVisit, pk=vis_id)

    if (visit.patientlab_visit.filter(closed=False).exists() or
        visit.patientreferral_visit.filter(closed=False).exists() or
        visit.dentistreport_visit.filter(closed=False).exists() or
        visit.patienttreatment_visit.filter(closed=False).exists()):
        messages.error(request, 'Patient visit has open items')
        return redirect('patients:listallpatientvisits')

    if request.method == 'POST':
        try:
            with transaction.atomic():
                perform_archiving(visit.id)
            messages.success(request, 'Patient visit archived')
            return redirect('patients:listallpatientvisits')
        except Exception as e:
            messages.error(request, f'Error:- {e}')
            return redirect(request.path)
    return render(request, 'patients/archive_visit.html', {'h_visit': visit})

# View archived visit
@login_required
def view_archived_visit(request, vis_id):

    archived_visit = get_object_or_404(ArchivedPatientVisit, pk=vis_id)
    form = ArchivedPatientVisitReadOnlyForm(instance=archived_visit)

    for field in form.fields.values():
        field.disabled = True

    context = {
        'h_form': form,
        'h_archivedvisit': archived_visit
    }
    return render(request, 'patients/view_archived_visit.html', context)


# List all archived visits
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators', 'Employees'])
def list_archived_visits(request):

    archivedvisits = ArchivedPatientVisit.objects.all().order_by('-archived')
    query = request.GET.get('item_name')

    if query:
        archivedvisits = archivedvisits.filter(
            Q(visit_title__icontains=query) |
            Q(patient__last_name__icontains=query) |
            Q(patient__first_name__icontains=query)
        ).distinct()
    else:
        archivedvisits = ArchivedPatientVisit.objects.all().order_by('-archived')

    paginator = Paginator(archivedvisits, per_page=10)
    page_number = request.GET.get('page')
    page_archivedvisits = paginator.get_page(page_number)

    context = {
        'h_archivedvisitstotal': archivedvisits.count(),
        'page_archivedvisits': page_archivedvisits
    }
    return render(request, 'patients/list_archivedvisits.html', context)
