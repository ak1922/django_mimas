import logging
from datetime import date
from django.db.models import Q
from django.urls import reverse
from datetime import timedelta
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import group_required
from accounts.models import AccountUser
from mimascompany.models import Dentist, Employee
from patients.forms import PatientAppointmentForm, ArchivedAppointmentsReadOnlyForm
from patients.models import Patient, PatientInsurance, PatientAppointment, ArchivedPatientAppointment


logger = logging.getLogger(__name__)


@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
# Create appointment
def create_appointment(request):
    """ Create patient appointment """

    if request.method == 'POST':
        form = PatientAppointmentForm(request.POST)

        if form.is_valid():
            new_appointment = form.save()
            messages.success(request, f'New appointment {new_appointment.appointment_title} created for {new_appointment.patient.full_name}')
            logger.info(f'New patient appointment {new_appointment.appointment_title} created by {request.user}')
            return redirect('patients:listallappointments')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {", ".join(errors)}')
                    logger.info(f'Patient Appointment Form Error:- {field} - {error}')
    else:
        form = PatientAppointmentForm()
    return render(request, 'patients/create_patientappointment.html', {'h_form': form})


# Create reocurring appointment
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def create_reocurring_appointment(request, pat_id):

    patient = get_object_or_404(Patient, pk=pat_id)
    dentist = Dentist.objects.filter(employee=patient.primary_dentist).first()
    insurance = PatientInsurance.objects.filter(patient=patient).first()
    branch_name = dentist.branch if dentist else None

    if request.method == 'POST':
        form = PatientAppointmentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # Extract special fields before popping
            number_appointments = data.get('number_appointments', 1)
            frequency = int(data.get('frequency', 1))
            base_date = data['appointment_date']
            base_title = data['appointment_title']

            for i in range(number_appointments):
                # Calculate new date
                current_date = base_date + timedelta(weeks=i * frequency)

                PatientAppointment.objects.create(
                    patient=patient,
                    dentist=dentist,
                    branch=branch_name,
                    insurance=insurance,
                    appointment_date=current_date,
                    appointment_title=f'{base_title} - Appt {i+1}',
                    appointment_time=data['appointment_time'],
                    reason=data['reason'],
                    status=data['status']
                )

            messages.success(request, f'{number_appointments} appointments created successfully.')
            logger.info(f'New patient appointments created by {request.user}')
            return redirect('patients:listpatients')
        else:
            for field, errors in form.errors.items():
                messages.error(request, f'{field}: {", ".join(errors)}')
    else:
        form = PatientAppointmentForm(initial={
            'patient': patient,
            'dentist': dentist,
            'branch': branch_name,
            'insurance': insurance,
        })

    context = {'h_form': form, 'patient': patient}
    return render(request, 'patients/create_patientappointment.html', context)


@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
# Create appointment from patient
def add_patient_appointment_patient(request, pat_id):

    patient = get_object_or_404(Patient, pk=pat_id)
    dentist_instance = Dentist.objects.filter(employee=patient.primary_dentist).first()
    appointment_branch = dentist_instance.branch
    current_user = get_object_or_404(AccountUser, username=request.user)

    if request.method == 'POST':
        form = PatientAppointmentForm(request.POST)

        if form.is_valid():
            new_appointment = form.save(commit=False)
            new_appointment.patient = patient
            new_appointment.dentist = dentist_instance
            new_appointment.branch = appointment_branch
            new_appointment.updated_by = current_user
            new_appointment.save()
            messages.success(request, f'Appointment created successfully for {patient.full_name}.')
            logger.info(f'Appointment created successfully for {patient.full_name} by {request.user}.')
            return redirect('patients:listpatients')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}:- {error}')
                    logger.error(f'Patient Appointment Form Error:- {field} - {error}')
    else:
        form = PatientAppointmentForm(initial={
            'patient': patient,
            'dentist': dentist_instance,
            'branch': appointment_branch,
        })

    context = {
        'h_form': form,
        'patient': patient
    }
    return render(request, 'patients/create_patientappointment.html', context)


# Edit appointment
@login_required
def edit_appointment(request, app_id):
    """ Edit patient appointment """

    next_url = request.GET.get('next', reverse('patients:listallappointments'))
    appointment = PatientAppointment.objects.get(pk=app_id)

    if request.method == 'POST':
        form = PatientAppointmentForm(request.POST, instance=appointment)

        if form.is_valid():
            current_user = AccountUser.objects.get(username=request.user)
            edited_appointment = form.save()
            edited_appointment.updated_by = current_user
            edited_appointment.save()
            messages.success(request, f'Appointment for {edited_appointment.patient} updated.')
            logger.info(f'Appointment for {edited_appointment.patient} updated by {request.user}.')
            return redirect(next_url)
        else:
            for error in form.errors.items():
                messages.error(request, f'Patient Appointment Form:- {error}')
                logger.error(f'Patient Appointment Form:- {error}')
    else:
        form = PatientAppointmentForm(instance=appointment)
    return render(request, 'patients/create_patientappointment.html', {'h_form': form})


# List appointments
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def list_all_appointments(request):
    """ List patient appointments """

    today = date.today()
    query = request.GET.get('item_name')
    appointments = PatientAppointment.objects.all().order_by('appointment_date')


    if query:
        appointments = appointments.filter(
            Q(appointment_title__icontains=query) |
            Q(patient__last_name__icontains=query) |
            Q(patient__first_name__icontains=query)
        ).distinct()
    else:
        appointments = PatientAppointment.objects.all().order_by('appointment_date')

    # Add pagination
    paginator = Paginator(appointments, per_page=10)
    page_number = request.GET.get('page')
    page_appointments = paginator.get_page(page_number)

    context = {
        'h_today': today,
        'h_appointscount': appointments.count(),
        'page_appointments': page_appointments
     }
    return render(request, 'patients/list_patientappointments.html', context)


# Patient appointments
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def list_patient_appointments(request, pat_id):
    """ List appointments for a particular patient """

    today = date.today()
    query = request.GET.get('item_name')
    patient = get_object_or_404(Patient, pk=pat_id)
    patient_appointments = PatientAppointment.objects.filter(patient=patient).order_by('-updated')

    if query:
        patient_appointments = patient_appointments.filter(
            Q(appointment_title__icontains=query) |
            Q(patient__last_name__icontains=query) |
            Q(patient__first_name__icontains=query)
        ).distinct()
    else:
        patient_appointments = PatientAppointment.objects.filter(patient=patient).order_by('-updated')

    paginator = Paginator(patient_appointments, per_page=10)
    page_number = request.GET.get('page')
    page_patientappointments = paginator.get_page(page_number)

    context = {
        'h_today': today,
        'h_patient': patient,
        'page_patientappointments': page_patientappointments,
        'h_appointmentstotal': patient_appointments.count(),
    }
    return render(request, 'patients/myappointments.html', context)


# Patient next appointment
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def view_next_appointment(request, pat_id):

    patient = get_object_or_404(Patient, pk=pat_id)
    next_appointment = PatientAppointment.objects.filter(patient=patient).first()
    form = PatientAppointmentForm(instance=next_appointment)

    for field in form.fields.values():
        field.disabled = True

    context = {
        'h_form': form,
        'h_nextappointment': next_appointment
    }
    return render(request, 'patients/view_patientappoitment.html', context)


# Patient appointment read only
@login_required
def view_appointment(request, app_id):

    appointment = PatientAppointment.objects.get(pk=app_id)
    form = PatientAppointmentForm(instance=appointment)

    for field in form.fields.values():
        field.disabled = True

    context = {
        'h_form': form,
        'h_appointment': appointment
    }
    return render(request, 'patients/view_patientappoitment.html', context)


# Delete appointment
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def delete_appointment(request, app_id):
    """ Delete patient appointment form database """

    appointment = PatientAppointment.objects.get(pk=app_id)

    if request.method == 'POST':
        logger.info(f'Patient appointment {appointment.appointment_title} delete requested by {request.user}')
        appointment.delete()
        messages.success(request, 'Patient appointment deleted.')
        logger.info(f'Patient appointment deleted by {request.user}')
    return redirect('patients:listallappointments')


# -------------------------- ARCHIVED APPOINTMENTS -----------------------------

# List archived visits
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def list_archived_appointments(request):

    query = request.GET.get('item_name')
    archived_appointments = ArchivedPatientAppointment.objects.all().order_by('-archived')

    if query:
        archived_appointments = archived_appointments.filter(
            Q(appointment_title__icontains=query) |
            Q(patient__last_name__icontains=query) |
            Q(patient__first_name__icontains=query)
        ).distinct()
    else:
        archived_appointments = ArchivedPatientAppointment.objects.all().order_by('-archived')

    paginator = Paginator(archived_appointments, per_page=10)
    page_number = request.GET.get('page')
    page_archivedappointments = paginator.get_page(page_number)

    context = {
        'page_archivedappointments': page_archivedappointments,
        'h_archivedcount': archived_appointments.count()
    }
    return render(request, 'patients/list_archivedappointments.html', context)


# View archived appointment
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def view_archived_appointment(request, app_id):

    appointment = get_object_or_404(ArchivedPatientAppointment, pk=app_id)
    form = ArchivedAppointmentsReadOnlyForm(instance=appointment)

    for field in form.fields.values():
        field.disabled = True
    return render(request, 'patients/view_archived_appointment.html', {'h_form': form})
