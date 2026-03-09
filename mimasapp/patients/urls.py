from django.urls import path

from .views.patients_center import patientscenter
from .views.patient_dashboard import patient_dashbaord
from .views.manage_patients import create_patient, edit_patient, list_patients, delete_patient, view_patient
from .views.manage_patientcontacts import create_patient_contact, list_patient_contacts, edit_patient_contact, \
    create_patient_contact_patient, view_patient_contact, delete_patient_contact
from .views.manage_patientdetails import create_patient_detail, edit_patient_detail, view_patient_detail, \
    list_patient_details, delete_patient_detail, create_patient_detail_patient
from .views.manage_patientinsurance import create_insurance, list_insurance, delete_insurance, edit_insurance, \
    create_patient_insurance_patient
from .views.manage_patientappointments import create_appointment, create_reocurring_appointment, edit_appointment, \
    delete_appointment, list_patient_appointments, list_all_appointments, add_patient_appointment_patient, \
    view_appointment, list_archived_appointments, view_archived_appointment
from .views.manage_patientvisits import create_patient_visit, list_patient_visits, list_all_patient_visits, \
    edit_patient_visit, view_patient_visit, view_archived_visit, view_visit_cost, delete_patient_visit, \
    list_archived_visits
from .views.manage_treatmentroom import create_treatment_room, list_treatment_rooms, edit_treatment_room, \
    view_treatment_room, delete_treatment_room
from .views.manage_visittasks import create_visit_task, delete_visit_task, edit_visit_task, list_visit_task, \
    view_visit_task, create_visit_task_visit

app_name = 'patients'

urlpatterns = [
    # Patient dashboard
    path('patientdashbaord/', patient_dashbaord, name='patientdashbaord'),
    # Patients center
    path('patientscenter/', patientscenter, name='patientscenter'),
    # Patients
    path('listpatients/', list_patients, name='listpatients'),
    path('createpatient/', create_patient, name='createpatient'),
    path('editpatient/<int:pat_id>/edit/', edit_patient, name='editpatient'),
    path('deletepatient/<int:pat_id>/delete', delete_patient, name='deletepatient'),
    path('viewpatient/<int:pat_id>/view/', view_patient, name='viewpatient'),
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
    # Treatment rooms
    path('createtreatmentroom', create_treatment_room, name='createtreatmentroom'),
    path('listtreatmentrooms/', list_treatment_rooms, name='listtreatmentrooms'),
    path('edittreatmentroom/<int:room_id>/edit/', edit_treatment_room, name='edittreatmentroom'),
    path('viewtreatmentroom/<int:room_id>/view/', view_treatment_room, name='viewtreatmentroom'),
    path('deletetreatmentroom/<int:room_id>/delete/', delete_treatment_room, name='deletetreatmentroom'),
    # Patient Appointment
    path('createappointment/', create_appointment, name='createappointment'),
    path('listallappointments/', list_all_appointments, name='listallappointments'),
    path('editappointment/<int:app_id>/edit/', edit_appointment, name='editappointment'),
    path('viewappointment/<int:app_id>/view/', view_appointment, name='viewappointment'),
    path('deleteappointment/<int:app_id>/delete/', delete_appointment, name='deleteappointment'),
    path('listpatientappointments/<int:pat_id>/list/', list_patient_appointments, name='listpatientappointments'),
    path('addappointmentpatient/<int:pat_id>/add/', add_patient_appointment_patient, name='addappointmentpatient'),
    path('createreocurringappointment/<int:pat_id>/create/', create_reocurring_appointment, name='createreocurringappointment'),
    # Archived Appointments
    path('listarchivedappointments/', list_archived_appointments, name='listarchivedappointments'),
    path('viewarchivedappointment/<int:app_id>/view/', view_archived_appointment, name='viewarchivedappointment'),
    # Patient Visit
    path('createpatientvisit/', create_patient_visit, name='createpatientvisit'),
    path('listpatientvisits/', list_patient_visits, name='listpatientvisits'),
    path('listallpatientvisits/', list_all_patient_visits, name='listallpatientvisits'),
    path('editpatientvisit/<int:vis_id>/edit/', edit_patient_visit, name='editpatientvisit'),
    path('viewpatientvisit/<int:vis_id>/view/', view_patient_visit, name='viewpatientvisit'),
    path('viewvisitcost/<int:vis_id>/view/', view_visit_cost, name='viewvisitcost'),
    path('deletepatientvisit/<int:vis_id>/delete/', delete_patient_visit, name='deletepatientvisit'),
    # Patient visit tasks
    path('createvisittask/', create_visit_task, name='createvisittask'),
    path('deletevisittask/<int:task_id>/delete/', delete_visit_task, name='deletevisittask'),
    path('editvisittask/<int:task_id>/edit/', edit_visit_task, name='editvisittask'),
    path('listvisittask/', list_visit_task, name='listvisittasks'),
    path('viewvisittask/<int:task_id>/view/', view_visit_task, name='viewvisittask'),
    path('createvisittaskvisit/<int:vis_id>/create/', create_visit_task_visit, name='createvisittaskvisit'),
    # Archived Visits
    path('listarchivedvisits/', list_archived_visits, name='listarchivedvisits'),
    path('viewarchivedvisit/<int:vis_id>/view/', view_archived_visit, name='viewarchivedvisit'),
    # Patient Billing
    # Archived Bills
]
