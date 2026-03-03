from datetime import date
from django.db.models import Q
from datetime import timedelta
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404


from accounts.decorators import group_required
from mimascompany.models.dentist_model import Dentist
from mimascompany.models.employee_model import Employee
from patients.models.patients_model import Patient
from patients.models.patientinsurance_model import PatientInsurance
from patients.forms.patientappointment_form import PatientAppointmentForm
from patients.models.patientappointment_model import PatientAppointment


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
            return redirect('patients:listallappointments')
        else:
            for field, errors in form.errors.items():
                messages.error(request, f'{field}: {", ".join(errors)}')
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
    branch_name = dentist.branch_name if dentist else None

    if request.method == 'POST':
        form = PatientAppointmentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # Extract special fields before popping
            number_appointments = data.get('number_appointments', 1)
            frequency = int(data.get('frequency', 1))
            base_date = data['appointment_date']
            base_title = data['appointment_title']

            # Iterate to create appointments
            for i in range(number_appointments):
                # Calculate new date
                current_date = base_date + timedelta(weeks=i * frequency)

                # Create the record directly with necessary data
                PatientAppointment.objects.create(
                    patient=patient,
                    dentist=dentist,
                    branch_name=branch_name,
                    insurance=insurance,
                    appointment_date=current_date,
                    appointment_title=f'{base_title} - Appt {i+1}',
                    appointment_time=data['appointment_time'],
                    reason=data['reason'],
                    confirmed=data['confirmed']
                )

            messages.success(request, f'{number_appointments} appointments created successfully.')
            return redirect('patients:listallappointments')
        else:
            for field, errors in form.errors.items():
                messages.error(request, f'{field}: {", ".join(errors)}')
    else:
        # Pre-fill form
        form = PatientAppointmentForm(initial={
            'patient': patient,
            'dentist': dentist,
            'branch_name': branch_name,
            'insurance': insurance,
        })

    context = {'h_form': form, 'patient': patient}
    return render(request, 'patients/create_reocurring_appointment.html', context)


@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
# Create appointment from patient
def add_patient_appointment_patient(request, pat_id):

    patient = get_object_or_404(Patient, pk=pat_id)
    patient_insurance = get_object_or_404(PatientInsurance, patient=patient)
    dentist_instance = Dentist.objects.filter(employee=patient.primary_dentist).first()
    appointment_branch = dentist_instance.branch_name
    current_user_instance = request.user

    if request.method == 'POST':
        form = PatientAppointmentForm(request.POST)

        if form.is_valid():
            new_appointment = form.save(commit=False)
            new_appointment.patient = patient
            new_appointment.dentist = dentist_instance
            new_appointment.branch = appointment_branch
            new_appointment.insurance = patient_insurance
            new_appointment.updated_by = current_user_instance
            new_appointment.save()
            messages.success(request, 'Appointment created successfully.')
            return redirect('patients:listpatients')
        else:
            messages.error(request, 'Invalid form data. Please check the details.')

    else:
        form = PatientAppointmentForm(initial={
            'patient': patient,
            'dentist': dentist_instance,
            'branch_name': appointment_branch,
            'insurance': patient_insurance
        })

    context = {
        'h_form': form,
        'patient': patient
    }
    return render(request, 'patients/create_patientappointment.html', context)


# Edit appointment
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def edit_appointment(request, app_id):
    """ Edit patient appointment """

    appointment = PatientAppointment.objects.get(pk=app_id)

    if request.method == 'POST':
        form = PatientAppointmentForm(request.POST, instance=appointment)

        if form.is_valid():
            current_user = Employee.objects.get(user=request.user)
            edited_appointment = form.save()
            edited_appointment.updated_by = current_user
            edited_appointment.save()
            return redirect('patients:listallappointments')

    else:
        form = PatientAppointmentForm(instance=appointment)
    return render(request, 'patients/create_patientappointment.html', {'h_form': form})


# List appointments
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def list_all_appointments(request):
    """ List patient appointments """

    appointments = PatientAppointment.objects.all().order_by('appointment_date')
    query = request.GET.get('item_name')

    if query:
        appointments = appointments.filter(
            Q(appointment_title__icontains=query) |
            Q(patient__first_name__icontains=query) |
            Q(patient__last_name__icontains=query)
        ).distinct()
    else:
        appointments = PatientAppointment.objects.all().order_by('appointment_date')

    # Add pagination
    paginator = Paginator(appointments, per_page=10)
    page_number = request.GET.get('page')
    page_appointments = paginator.get_page(page_number)

    context = {
        'h_query': query,
        'h_appointscount': appointments.count(),
        'page_appointments': page_appointments
     }
    return render(request, 'patients/list_patientappointments.html', context)


# Patient appointments
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def list_patient_appointments(request, pat_id):

    today = date.today()
    patient = get_object_or_404(Patient, pk=pat_id)
    patient_appointments = PatientAppointment.objects.filter(patient=patient)

    context = {
        'h_today': today,
        'h_patient': patient,
        'h_patientappointments': patient_appointments
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
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
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
        appointment.delete()
        messages.success(request, 'Patient appointment deleted.')
    return redirect('patients:listallappointments')
