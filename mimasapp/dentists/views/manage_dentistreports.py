import logging
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from accounts.decorators import group_required
from mimascompany.models.employee_model import Employee
from patients.models import Patient, PatientVisit
from dentists.models import DentistReport, ArchivedDentistReport
from dentists.forms import DentistReportForm, ArchivedDentistReportForm


logger = logging.getLogger(__name__)


# Create dentist report
@login_required
@group_required(allowed_groups=['Dentists', 'Employees', 'Administrators'])
def create_dentist_report(request):

    if request.method == 'POST':
        form = DentistReportForm(request.POST)

        if form.is_valid():
            new_report = form.save()
            messages.success(request, f'New dentist report {new_report.report_title} created for patient {new_report.patient}.')
            logger.info(f'New dentist report {new_report.report_title} created for patient {new_report.patient}.')
            return redirect('dentists:listalldentistreports')
        else:
            messages.error(request, 'Invalid form.')
    else:
        form = DentistReportForm()

    context = {
        'h_form': form,
        'h_existing_report': None
    }
    return render(request, 'dentists/create_dentistreport.html', context)


# Create dentist report from patient visit
@login_required
@group_required(allowed_groups=['Dentists', 'Employees', 'Administrators'])
def create_report_patient_visit(request, vis_id=None):
    """ Create dentist report for patient from list of patient visits table """

    visit = get_object_or_404(PatientVisit, pk=vis_id)

    if request.method == 'POST':
        form = DentistReportForm(request.POST)
        if form.is_valid():
            new_report = form.save(commit=False)
            new_report.patient = visit.patient
            new_report.dentist = visit.dentist
            new_report.branch = visit.branch
            new_report.insurance = visit.insurance
            new_report.appointment = visit.appointment
            new_report.visit = visit
            new_report.save()
            messages.success(request, f'New Dentist Report created for Patient {visit.patient}.')
            logger.info(f'New Dentist Report created for Patient {visit.patient} with visit {visit.visit_title} by {request.user}.')
            return redirect('patients:listallpatientvisits')
        else:
            messages.error(request, 'Invalid form')
    else:
        form = DentistReportForm(initial={
            'patient': visit.patient,
            'dentist': visit.dentist,
            'branch': visit.branch,
            'insurance': visit.insurance,
            'appointment': visit.appointment,
            'visit': visit
        })

    context = {
        'h_form': form,
        'h_patientvisit': visit
    }
    return render(request, 'dentists/create_dentistreport.html', context)


# Edit dentist report
@login_required
@group_required(allowed_groups=['Dentists', 'Employees', 'Administrators'])
def edit_dentist_report(request, rep_id):

    report = get_object_or_404(DentistReport, pk=rep_id)

    if request.method == 'POST':
        form = DentistReportForm(request.POST, instance=report)

        if form.is_valid():
            current_user = get_object_or_404(Employee, user=request.user)
            edited_report = form.save(commit=False)
            edited_report.updated_by = current_user
            edited_report.save()
            messages.success(request, f'Report {edited_report.report_title} for patient {edited_report.patient} updated.')
            logger.info(f'Report {edited_report.report_title} for patient {edited_report.patient} updated by {request.user}.')
            return redirect('dentists:listalldentistreports')
        else:
            messages.error(request, 'Invalid Report.')
            return redirect(request.path)
    else:
        form = DentistReportForm(instance=report)
    return render(request, 'dentists/create_dentistreport.html', {'h_form': form})


# View report
@login_required
@group_required(allowed_groups=['Dentists', 'Employees', 'Administrators'])
def view_dentist_report(request, rep_id):

    report = get_object_or_404(DentistReport, pk=rep_id)
    form = DentistReportForm(instance=report)

    for field in form.fields.values():
        field.disabled = True

    context = {
        'h_form': form,
        'h_existing_report': report,
    }
    return render(request, 'dentists/create_dentistreport.html', context)


# List dentist reports
@login_required
@group_required(allowed_groups=['Dentists', 'Employees', 'Administrators'])
def list_all_dentist_reports(request):

    query = request.GET.get('item_name')
    allreports = DentistReport.objects.all().order_by('created')

    if query:
        allreports = allreports.filter(
            Q(report_title__icontains=query) |
            Q(patient__last_name__icontains=query) |
            Q(patient__first_name__icontains=query) |
            Q(dentist__employee__first_name__icontains=query) |
            Q(patient__patientvisit_patient__visit_title=query) |
            Q(patient__patientappointment_patient__appointment_title__icontains=query)
        ).distinct()
    else:
        allreports = DentistReport.objects.all().order_by('created')

    paginator = Paginator(allreports, per_page=10)
    page_number = request.GET.get('page')
    page_allreports = paginator.get_page(page_number)

    context = {
        'page_allreports': page_allreports,
        'h_allreportscount': allreports.count()
    }

    return render(request, 'dentists/list_dentistsreports.html', context)


# List reports for patient
@login_required
@group_required(allowed_groups=['Dentists', 'Employees', 'Administrators'])
def list_patient_reports(request, pat_id):

    patient = get_object_or_404(Patient, pk=pat_id)
    patient_reports = DentistReport.objects.filter(patient=patient).order_by('created')

    context = {
        'h_patient': patient,
        'page_allreports': patient_reports
    }
    return render(request, 'dentists/list_onepatient_reports.html', context)


# Delete dentist report
@login_required
@group_required(allowed_groups=['Dentists', 'Employees', 'Administrators'])
def delete_dentist_report(request, rep_id):

    report = get_object_or_404(DentistReport, pk=rep_id)

    if request.method == 'POST':
        report.delete()
        messages.success(request, 'Dentist report deleted.')
    return redirect('dentists:listalldentistreports')


# -------------------------- Archived reports ----------------------

# view archived report
@login_required
def view_archived_report(request, rep_id):

    archived_report = get_object_or_404(ArchivedDentistReport, pk=rep_id)
    form = ArchivedDentistReportForm(instance=archived_report)

    context = {
        'h_form': form,
        'h_archivedreport': archived_report
    }
    return render(request, 'dentists/view_archivedreport.html', context)


# List archived reports
@login_required
@group_required(allowed_groups=['Dentists', 'Employees', 'Administrators'])
def list_all_archived_reports(request):

    allreports = ArchivedDentistReport.objects.all().order_by('archived')
    query = request.GET.get('item_name')

    if query:
        allreports = allreports.filter(
            Q(patient__icontains=query) |
            Q(dentist__icontains=query) |
            Q(report_title__icontains=query)
        ).distinct()
    else:
        allreports = ArchivedDentistReport.objects.all().order_by('archived')

    paginator = Paginator(allreports, per_page=10)
    page_number = request.GET.get('page')
    page_allreports = paginator.get_page(page_number)

    context = {
        'page_allreports': page_allreports,
        'h_allreportscount': allreports.count()
    }
    return render(request, 'dentists/list_archivedreports.html', context)
