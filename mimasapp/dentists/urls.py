from django.urls import path

from .views.dentist_office import dentist_office
from .views.dentist_dashboard import dentist_dashboard
from .views.manage_patientlabs import create_patient_lab, create_lab_patient_visit, list_patient_labs, list_all_patients_labs, \
    list_all_archived_labs, edit_patient_lab, view_patient_lab, view_archived_lab, delete_patient_lab
from .views.manage_patienttreatments import create_treatment, create_treatment_patient_visit, list_patient_treatments, \
    list_all_treatments, list_all_archived_treatments, edit_treatment, view_archived_treatment, view_treatment, delete_treatment
from .views.manage_patientreferrals import create_referral, create_referral_patient_visit, list_patient_referrals, \
    list_all_patient_referrals, list_all_archived_referrals, view_referral, view_archived_referral, edit_referral, delete_referral
from .views.manage_dentistreports import list_patient_reports, list_all_dentist_reports, list_all_archived_reports, \
    create_report_patient_visit, create_dentist_report, view_dentist_report, view_archived_report, delete_dentist_report, \
    edit_dentist_report


app_name = 'dentists'

urlpatterns = [
    # Dentist office
    path('dentistoffice/', dentist_office, name='dentistoffice'),
    # Dentist dashboard
    path('dentistdashboard/', dentist_dashboard, name='dentistdashboard'),
    # Patient labs
    path('createpatientlab/', create_patient_lab, name='createpatientlab'),
    path('listallpatientslabs/', list_all_patients_labs, name='listallpatientslabs'),
    path('viewpatientlab/<int:lab_id>/view/', view_patient_lab, name='viewpatientlab'),
    path('editpatientlab/<int:lab_id>/edit/', edit_patient_lab, name='editpatientlab'),
    path('listpatientlabs/<int:pat_id>/list/', list_patient_labs, name='listpatientlabs'),
    path('deletepatientlab/<int:lab_id>/delete/', delete_patient_lab, name='deletepatientlab'),
    path('createlabpatientvisit/<int:vis_id>/create/', create_lab_patient_visit, name='createlabpatientvisit'),
    # Archived Labs
    path('listallarchivedlabs/', list_all_archived_labs, name='listallarchivedlabs'),
    path('viewarchivedlab/<int:lab_id>/view/', view_archived_lab, name='viewarchivedlab'),
    # Patient referrals
    path('createreferral/', create_referral, name='createreferral'),
    path('viewreferral/<int:ref_id>/view/', view_referral, name='viewreferral'),
    path('editreferral/<int:ref_id>/edit/', edit_referral, name='editreferral'),
    path('deletereferral/<int:ref_id>/delete/', delete_referral, name='deletereferral'),
    path('listallpatientreferrals/', list_all_patient_referrals, name='listallpatientreferrals'),
    path('listpatientreferrals/<int:pat_id>/list/', list_patient_referrals, name='listpatientreferrals'),
    path('createreferralpatientvisit/<int:vis_id>/create/', create_referral_patient_visit, name='createreferralpatientvisit'),
    # Archived referrals
    path('listallarchivedreferrals/', list_all_archived_referrals, name='listallarchivedreferrals'),
    path('viewarchivedreferral/<int:ref_id>/view/', view_archived_referral, name='viewarchivedreferral'),
    # Patient treatments
    path('createtreatment/', create_treatment, name='createtreatment'),
    path('listalltreatments/', list_all_treatments, name='listalltreatments'),
    path('viewtreatment/<int:tre_id>/view/', view_treatment, name='viewtreatment'),
    path('edittreatment/<int:tre_id>/edit/', edit_treatment, name='edittreatment'),
    path('deletetreatment/<int:tre_id>/delete', delete_treatment, name='deletetreatment'),
    path('listpatienttreatments/<int:pat_id>/list/', list_patient_treatments, name='listpatienttreatments'),
    path('createtreatmentpatientvisit/<int:vis_id>/create/', create_treatment_patient_visit, name='createtreatmentpatientvisit'),
    # Archived Treatments
    path('viewarchivedtreatment/<int:tre_id>/view/', view_archived_treatment, name='viewarchivedtreatment'),
    path('listallarchivedtreatments/', list_all_archived_treatments, name='listallarchivedtreatments'),
    # Dentist reports
    path('createdentistreport/', create_dentist_report, name='createdentistreport'),
    path('viewdentistreport/<int:rep_id>/view/', view_dentist_report, name='viewdentistreport'),
    path('deletedentistreport/<int:rep_id>/delete/', delete_dentist_report, name='deletedentistreport'),
    path('listpatientreports/<int:pat_id>/list/', list_patient_reports, name='listpatientreports'),
    path('editdentistreport/<int:rep_id>/edit/', edit_dentist_report, name='editdentistreport'),
    path('listalldentistreports/', list_all_dentist_reports, name='listalldentistreports'),
    path('createreportpatientvisit/<int:vis_id>/create/', create_report_patient_visit, name='createreportpatientvisit'),
    # Archived Reports
    path('viewarchivedreport/<int:rep_id>/view/', view_archived_report, name='viewarchivedreport'),
    path('listallarchivedreports/', list_all_archived_reports, name='listallarchivedreports'),
]
