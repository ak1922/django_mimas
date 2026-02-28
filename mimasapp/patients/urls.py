from django.urls import path

from .views.patients_center import patientscenter
from .views.manage_patients import create_patient, edit_patient, list_patients, delete_patient, view_patient
from .views.manage_patientcontacts import create_patient_contact, list_patient_contacts, edit_patient_contact, \
    create_patient_contact_patient, view_patient_contact, delete_patient_contact


app_name = 'patients'

urlpatterns = [
    path('patientscenter/', patientscenter, name='patientscenter'),
    # Patients
    path('listpatients/', list_patients, name='listpatients'),
    path('createpatient/', create_patient, name='createpatient'),
    path('editpatient/<uuid:pat_id>/edit/', edit_patient, name='editpatient'),
    path('deletepatient/<uuid:pat_id>/delete', delete_patient, name='deletepatient'),
    path('viewpatient/<uuid:pat_id>/view/', view_patient, name='viewpatient'),
    # Patient Dashboard
    # Patient Contact
    path('createpatientcontact/', create_patient_contact, name='createpatientcontact'),
    path('listpatientcontacts/', list_patient_contacts, name='listpatientcontacts'),
    path('editpatientcontact/<uuid:con_id>/edit/', edit_patient_contact, name='editpatientcontact'),
    path('viewpatientcontact/<uuid:con_id>/view/', view_patient_contact, name='viewpatientcontact'),
    path('deletepatientcontact/<uuid:con_id>/delete/', delete_patient_contact, name='deletepatientcontact'),
    path('createcontactpatient/<uuid:pat_id>/create/', create_patient_contact_patient, name='createcontactpatient'),
    # Patient Details
    # Patient Insurance
    # Patient Appointment
    # Archived Appointments
    # Patient Visit
    # Archived Visits
    # Patient Billing
    # Archived Bills
]
