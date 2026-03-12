import logging
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import group_required
from mimascompany.models.employee_model import Employee
from dentists.forms.patientlab_forms import PatientLabForm
from dentists.forms.archived_forms import ArchivedPatientLabForm
from patients.models.patients_model import Patient
from patients.models.patientvisit_models import PatientVisit
from patients.models.patientlab_model import PatientLab
from patients.models.archivedlab_model import ArchivedPatientLab


logger = logging.getLogger(__name__)


# Create patient lab
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def create_patient_lab(request):

    next_url = request.GET.get('next', reverse('dentists:listallpatientslabs'))
    if request.method == 'POST':
        form = PatientLabForm(request.POST)

        if not request.user.user_type == 'Dentists':
            for field in form.fields.values():
                field.disabled = True
        else:
            if form.is_valid():
                new_lab = form.save()
                messages.success(request, f'New lab {new_lab.lab_title} created for {new_lab.patient}')
                logger.info(f'New lab {new_lab.lab_title} created for {new_lab.patient} by {request.user}.')
                return redirect(next_url)
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'Patient Lab Form Error:- {field} - {error}')
                        logger.info(f'Patient Lab Form Error:- {field} - {error}')
    else:
        form = PatientLabForm()
        if not request.user.user_type == 'Dentists':
            for field in form.fields.values():
                field.disabled = True

    context = {
        'h_form': form,
        'h_existing_lab': None
    }
    return render(request, 'dentists/create_lab.html', context)


# Add lab from patient visit

@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def create_lab_patient_visit(request, vis_id=None):
    """
        Create patient lab from patient visits.
    """
    visit = get_object_or_404(PatientVisit, pk=vis_id)

    if request.method == 'POST':
        form = PatientLabForm(request.POST)

        if form.is_valid():
            new_lab = form.save(commit=False)
            new_lab.patient = visit.patient
            new_lab.dentist = visit.dentist
            new_lab.branch = visit.branch
            new_lab.insurance = visit.insurance or None
            new_lab.appointment = visit.appointment or None
            new_lab.visit = visit
            new_lab.save()
            messages.success(request, f'New patient lab created for {visit.patient}.')
            logger.info(f'New patient lab created for {visit.patient}.')
            return redirect('patients:listallpatientvisits')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Patient Lab Form Error:- {field} - {error}')
                    logger.info(f'Patient Lab Form Error:- {field} - {error}')
    else:
        form = PatientLabForm(initial={
            'patient': visit.patient,
            'dentist': visit.dentist,
            'branch': visit.branch,
            'insurance': visit.insurance,
            'appointment': visit.appointment,
            'visit': visit,
        })

    context = {
        'h_form': form,
        'h_existing_lab': None
    }
    return render(request, 'dentists/create_lab.html', context)


# Edit lab
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def edit_patient_lab(request, lab_id):

    lab = get_object_or_404(PatientLab, pk=lab_id)
    next_url = request.GET.get('next', reverse('dentists:listallpatientslabs'))

    if request.method == 'POST':
        form = PatientLabForm(request.POST, instance=lab)
        if form.is_valid():
            current_user = Employee.objects.get(user=request.user)
            edited_lab = form.save(commit=False)
            edited_lab.updated_by = current_user
            edited_lab.save()
            messages.success(request, f'Lab {edited_lab.lab_title} for patient {edited_lab.patient} updated.')
            logger.info(f'Lab {edited_lab.lab_title} for patient {edited_lab.patient} updated.')
            return redirect(next_url)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Patient Lab Form Error:- {field} - {error}')
                    logger.info(f'Patient Lab Form Error:- {field} - {error}')
    else:
        form = PatientLabForm(instance=lab)

    return render(request, 'dentists/create_lab.html', {'h_form': form})


# View lab
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def view_patient_lab(request, lab_id):

    lab = PatientLab.objects.get(pk=lab_id)
    form = PatientLabForm(instance=lab)

    for field in form.fields.values():
        field.disabled = True

    context = {
        'h_form': form,
        'h_existing_lab': lab
    }
    return render(request, 'dentists/create_lab.html', context)


# List patient lab
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def list_all_patients_labs(request):

    alllabs = PatientLab.objects.all().order_by('created')
    query = request.GET.get('item_name')

    if query:
        alllabs = alllabs.filter(
            Q(lab_title__icontains=query) |
            Q(lab_name__icontains=query) |
            Q(patient__first_name__icontains=query) |
            Q(patient__last_name__icontains=query)
        ).distinct()
    else:
        alllabs = PatientLab.objects.all().order_by('created')

    paginator = Paginator(alllabs, 10)
    page_number = request.GET.get('page')
    page_alllabs = paginator.get_page(page_number)

    context = {
        'page_alllabs': page_alllabs,
        'h_labscount': alllabs.count(),
    }
    return render(request, 'dentists/list_labs.html', context)


# List labs for a patient
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def list_patient_labs(request, pat_id):

    query = request.GET.get('item_name')
    patient = get_object_or_404(Patient, pk=pat_id)
    patientlabs = PatientLab.objects.filter(patient=patient).order_by('created')

    if query:
        patientlabs = patientlabs.filter(
            Q(lab_title__icontains=query)
        ).distinct()
    else:
        patientlabs = PatientLab.objects.filter(patient=patient).order_by('created')

    context = {
        'h_patient': patient,
        'page_alllabs': patientlabs,
        'h_labscount': patientlabs.count()
    }
    return render(request, 'dentists/list_onepatient_labs.html', context)


# Delete patient lab
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def delete_patient_lab(request, lab_id):

    lab = PatientLab.objects.get(pk=lab_id)

    if request.method == 'POST':
        lab.delete()
        messages.success(request, 'Lab information deleted.')
    return redirect('dentists:listallpatientlabs')



# ------------------------------- Archived Labs -------------------------------------------

# View archived lab
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def view_archived_lab(request, lab_id):

    archived_lab = ArchivedPatientLab.objects.get(pk=lab_id)
    form = ArchivedPatientLabForm(instance=archived_lab)

    for field in form.fields.values():
        field.disabled = True

    context = {
        'h_form': form,
        'h_archivedlab': archived_lab
    }
    return render(request, 'dentists/view_archivedlab.html', context)


# List archived labs
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def list_all_archived_labs(request):

    query = request.POST.get('item_name')
    allarchivedlabs = ArchivedPatientLab.objects.all().order_by('-archived_on')

    if query:
        allarchivedlabs = allarchivedlabs.filter(
            Q(lab_title__icontains=query) |
            Q(lab_name__icontains=query) |
            Q(patient__first_name__icontains=query) |
            Q(patient__last_name__icontains=query)
        ).distinct()
    else:
        allarchivedlabs = ArchivedPatientLab.objects.all().order_by('-archived_on')

    paginator = Paginator(allarchivedlabs, 10)
    page_number = request.GET.get('page')
    page_allarchivedlabs = paginator.get_page(page_number)

    context = {
        'page_allarchivedlabs': page_allarchivedlabs,
        'h_allarchicedcount': allarchivedlabs.count(),
    }
    return render(request, 'dentists/list_archivedlabs.html', context)
