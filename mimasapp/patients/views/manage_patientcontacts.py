from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import group_required
from mimascompany.models.employee_model import Employee
from patients.models.patients_model import Patient
from patients.models.patientcontact_model import PatientContact
from patients.forms.patientscontact_form import PatientContactForm


# Add patients contact
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def create_patient_contact(request):

    next_url = request.GET.get('next', reverse('patients:listpatientcontacts'))

    if request.method == 'POST':
        form = PatientContactForm(request.POST)

        if form.is_valid():
            new_contact = form.save()
            messages.success(request, f'New contact created for {new_contact.patient.full_name}')
            return redirect(next_url)
        else:
            messages.error(request, 'Issues creating new contact.')

    else:
        form = PatientContactForm()
    return render(request, 'patients/create_patientcontact.html', {'h_form': form})


@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def create_patient_contact_patient(request, pat_id=None):
    """ Create patient contact from list of patients table """

    next_url = request.GET.get('next', reverse('patients:listpatientcontacts'))

    patient_contact = None
    if pat_id:
        new_patient = get_object_or_404(Patient, pk=pat_id)

        try:
            patient_contact = new_patient.patientcontact_patient
        except PatientContact.DoesNotExist:
            patient_contact = PatientContact(patient=new_patient)

    if request.method == 'POST':
        form = PatientContactForm(request.POST, instance=patient_contact)

        if form.is_valid():
            new_contact = form.save()
            messages.success(request, f'Patient information for {new_contact.patient.full_name} updated.')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid form')

    else:
        form = PatientContactForm(instance=patient_contact)
    return render(request, 'patients/create_patientcontact.html', {'h_form': form})


# List contacts
@login_required()
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def list_patient_contacts(request):

    allpatients = Patient.objects.all().count()
    allcontacts = PatientContact.objects.all().order_by('created')

    paginator = Paginator(allcontacts, per_page=10)
    page_number = request.GET.get('page')
    page_contacts = paginator.get_page(page_number)

    context = {
        'h_allpatients': allpatients,
        'page_contacts': page_contacts,
        'h_allcontactstotal': allcontacts.count(),
    }
    return render(request, 'patients/list_patientcontacts.html', context)


# Update patient contact for patients only
# @login_required
# @group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
# def update_contact_patient(request, pat_id):
#     """ Update patient contact for patients """
#
#     patient = PatientContact.objects.get(pk=pat_id)
#
#     if request.method == 'POST':
#         form = PatientContactForm(request.POST, instance=patient)
#         form.fields['patient'].disabled = True
#
#         if form.is_valid():
#             current_patient = Employee.objects.get(user=request.user)
#             edited_contact = form.save()
#             edited_contact.updated_ny = current_patient
#             edited_contact.save()
#             return redirect('patients:listpatients')
#             # return redirect('patients:patientdashboard', patient.pk)
#         else:
#             messages.error(request, 'Issues with contact update.')
#
#     else:
#         form = PatientContactForm(instance=patient)
#     return render(request, 'patients/update_contact_patientonly.html', {'h_form': form})


# Edit contact
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def edit_patient_contact(request, con_id):

    contact = PatientContact.objects.get(pk=con_id)

    if request.method == 'POST':
        form = PatientContactForm(request.POST, instance=contact)

        if form.is_valid():
            current_user = Employee.objects.get(user=request.user)
            edited_contact = form.save(commit=False)
            edited_contact.updated_by = current_user
            edited_contact.save()
            return redirect('patients:listpatientcontacts')
        else:
            messages.error(request, 'Issues updating patient contact.')

    else:
        form = PatientContactForm(instance=contact)
    return render(request, 'patients/create_patientcontact.html', {'h_form': form})


# View patient contact
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def view_patient_contact(request, con_id):

    patient_contact = get_object_or_404(PatientContact, pk=con_id)
    form = PatientContactForm(instance=patient_contact)

    for field in form.fields.values():
        field.disabled = True

    context = {
        'h_form': form,
        'h_patient': patient_contact
    }
    return render(request, 'patients/view_patientcontact.html', context)


# Delete contact
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def delete_patient_contact(request, con_id):

    contact = PatientContact.objects.get(pk=con_id)

    if request.method == 'POST':
        contact.delete()
    return redirect('patients:listpatientcontacts')
