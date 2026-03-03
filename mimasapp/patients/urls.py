from django.urls import path

from .views.patients_center import patientscenter
from .views.manage_patients import create_patient, edit_patient, list_patients, delete_patient, view_patient
from .views.manage_patientcontacts import create_patient_contact, list_patient_contacts, edit_patient_contact, \
    create_patient_contact_patient, view_patient_contact, delete_patient_contact
from .views.manage_patientdetails import create_patient_detail, edit_patient_detail, view_patient_detail, \
    list_patient_details, delete_patient_detail, create_patient_detail_patient
from .views.manage_patientinsurance import create_insurance, list_insurance, delete_insurance, edit_insurance, \
    create_patient_insurance_patient
from .views.manage_patientappointments import create_appointment, create_reocurring_appointment, edit_appointment, \
    delete_appointment, list_patient_appointments, list_all_appointments, add_patient_appointment_patient

app_name = 'patients'

urlpatterns = [
    path('patientscenter/', patientscenter, name='patientscenter'),
    # Patients
    path('listpatients/', list_patients, name='listpatients'),
    path('createpatient/', create_patient, name='createpatient'),
    path('editpatient/<int:pat_id>/edit/', edit_patient, name='editpatient'),
    path('deletepatient/<int:pat_id>/delete', delete_patient, name='deletepatient'),
    path('viewpatient/<int:pat_id>/view/', view_patient, name='viewpatient'),
    # Patient Dashboard
    # Patient Contact
    path('createpatientcontact/', create_patient_contact, name='createpatientcontact'),
    path('listpatientcontacts/', list_patient_contacts, name='listpatientcontacts'),
    path('editpatientcontact/<int:con_id>/edit/', edit_patient_contact, name='editpatientcontact'),
    path('viewpatientcontact/<int:con_id>/view/', view_patient_contact, name='viewpatientcontact'),
    path('deletepatientcontact/<int:con_id>/delete/', delete_patient_contact, name='deletepatientcontact'),
    path('createcontactpatient/<int:pat_id>/create/', create_patient_contact_patient, name='createcontactpatient'),
    # Patient Details
    path('createpatientdetail/', create_patient_detail, name='createpatientdetail'),
    path('listpatientdetails/', list_patient_details, name='listpatientdetails'),
    path('editpatientdetail/<int:det_id>/edit/', edit_patient_detail, name='editpatientdetail'),
    path('viewpatientdetail/<int:det_id>/view/', view_patient_detail, name='viewpatientdetail'),
    path('deletepatientdetail/<int:det_id>/delete/', delete_patient_detail, name='deletepatientdetail'),
    path('createpatientdetailpatient/<int:pat_id>/delete/', create_patient_detail_patient, name='createpatientdetailpatient'),
    # Patient Insurance
    path('listinsurance/', list_insurance, name='listinsurance'),
    path('createinsurance/', create_insurance, name='createinsurance'),
    path('editinsurance/<int:ins_id>/edit/', edit_insurance, name='editinsurance'),
    path('deleteinsurance/<int:ins_id>/delete/', delete_insurance, name='deleteinsurance'),
    path('createinsurancepatient/<int:pat_id>/create/', create_patient_insurance_patient, name='createinsurancepatient'),
    # Patient Appointment
    path('createappointment/', create_appointment, name='createappointment'),
    path('listallappointments/', list_all_appointments, name='listallappointments'),
    path('editappointment/<int:app_id>/edit/', edit_appointment, name='editappointment'),
    path('deleteappointment/<int:app_id>/delete/', delete_appointment, name='deleteappointment'),
    path('listpatientappointments/<int:pat_id>/list/', list_patient_appointments, name='listpatientappointments'),
    path('addappointmentpatient/<int:pat_id>/add/', add_patient_appointment_patient, name='addappointmentpatient'),
    path('createreocurringappointment/<int:pat_id>/create/', create_reocurring_appointment, name='createreocurringappointment'),
    # Archived Appointments
    # Patient Visit
    # Archived Visits
    # Patient Billing
    # Archived Bills
]
