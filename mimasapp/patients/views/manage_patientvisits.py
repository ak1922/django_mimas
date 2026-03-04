# from datetime import date
# from django.urls import reverse
# from django.db import transaction
# from django.contrib import messages
# from django.db.models import Sum, Q
# from django.core.paginator import Paginator
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect, get_object_or_404
# from django.core.exceptions import ObjectDoesNotExist, ValidationError
#
# from dentists.models import DentistReport
# from marscompany.decorators import role_required
# from marscompany.models.employees_model import Employee
# from patients.utils import perform_archive_tasks
# from patients.models.patient_model import Patient
# from patients.models.patientlab_model import PatientLab
# from patients.models.patientbill_model import PatientBill
# from patients.models.auxilary_models import PatientsMessage
# from patients.models.patientreferral_model import PatientReferral
# from patients.models.patienttreatment_model import PatientTreatment
# from patients.forms import PatientVisitForm, ArchivedPatientVisitForm, ArchivedVisitServiceDetailForm
# from patients.models.patientvisit_model import PatientVisit, ArchivedPatientVisit, ArchivedVisitServiceDetail
#
#
# # Create visit
# @login_required
# @role_required(allowed_roles=['Dentist', 'Admin', 'Employee' ])
# def create_patient_visit(request):
#
#     if request.method == 'POST':
#         form = PatientVisitForm(request.POST)
#         if form.is_valid():
#             new_visit = form.save(commit=False)
#             new_visit.save()
#             form.save_m2m()
#             messages.success(request, f'New visit {new_visit.visit_title} created for {new_visit.patient.patient_name}')
#             print(request.user.user_type)
#             return redirect('patients:listallpatientvisits')
#         else:
#             messages.error(request, 'Errors creating new patient visit.')
#     else:
#         form = PatientVisitForm()
#     return render(request, 'patients/create_patientvisit.html', {'h_form': form})
#
#
# # Edit visit
# @login_required
# @role_required(allowed_roles=['Dentist', 'Admin', 'Employee'])
# def edit_patient_visit(request, vis_id):
#     """
#         manage visits
#     """
#     visit = get_object_or_404(PatientVisit, pk=vis_id)
#     original_status = visit.status
#     has_unpaid_bill = PatientBill.objects.filter(visit_title__id=visit.id, is_paid=False).exists()
#     next_url = request.GET.get('next', reverse('patients:listallpatientvisits'))
#
#     if request.method == 'POST':
#             form = PatientVisitForm(request.POST, instance=visit)
#             if form.is_valid():
#                 current_user = Employee.objects.get(user=request.user)
#                 edited_visit = form.save(commit=False)
#                 edited_visit.modified_by = current_user
#
#                 with transaction.atomic():
#                     if edited_visit.status == 'Closed' and original_status != 'Closed':
#                         if has_unpaid_bill:
#                             edited_visit.status = 'Completed'
#                             edited_visit.save()
#                             form.save_m2m()
#                             messages.error(request, 'Patient bill for visit is unpaid. Status set to Completed, not Closed.')
#                             return redirect('patients:listpatientbills')
#                         else:
#                             edited_visit.save()
#                             form.save_m2m()
#                     else:
#                         # General case, save the instance and M2M data
#                         edited_visit.save()
#                         form.save_m2m()
#                         PatientsMessage.objects.create(
#                             visit=edited_visit,
#                             message=f"Patient Visit Message:- {edited_visit.visit_title} for patient {edited_visit.patient.patient_name} status updated."
#                         )
#                         messages.success(request, "Visit updated successfully.")
#                         return redirect(next_url) # Redirect to referrer
#
#             else:
#                 for field, errors in form.errors.items():
#                     for error in errors:
#                         messages.error(request, f'Patient Visit Form Error:- {field}: {error}')
#                 messages.error(request, 'Form validation issues occurred.')
#
#     else:
#         form = PatientVisitForm(instance=visit)
#     return render(request, 'patients/create_patientvisit.html', {'h_form': form})
#
#
# # Patient visit read only
# @login_required
# @role_required(allowed_roles=['Employee', 'Dentist', 'Admin', 'Patient'])
# def read_patient_visit(request, vis_id):
#
#     visit = PatientVisit.objects.get(pk=vis_id)
#     form = PatientVisitForm(instance=visit)
#
#     for field in form.fields.values():
#         field.disabled = True
#
#     lab = None
#     report = None
#     referral = None
#     treatment = None
#
#     try:
#         lab = visit.patientlab_visittitle.order_by('-id').first()
#     except ObjectDoesNotExist:
#         lab = None
#     try:
#         report = visit.dentistreport_visittitle.order_by('-id').first()
#     except ObjectDoesNotExist:
#         report = None
#     try:
#         referral = visit.patientreferral_visittitle.order_by('-id').first()
#     except ObjectDoesNotExist:
#         referral = None
#     try:
#         treatment = visit.patienttreatment_visittitle.order_by('-id').first()
#     except ObjectDoesNotExist:
#         treatment = None
#
#     # referer = request.META.get('HTTP_REFERER', '')
#     # if 'dentistpatients' in referer:
#     #     return redirect('dentists:dentistdashboard')
#
#     context = {
#         'h_lab': lab,
#         'h_form': form,
#         'h_visit': visit,
#         'h_report': report,
#         'h_referral': referral,
#         'h_treatment': treatment
#     }
#     return render(request, 'patients/read_patientvisit.html', context)
#
#
# # # Archive visit
# # @login_required
# # @role_required(allowed_roles=['Employee', 'Dentist', 'Admin', 'Patient'])
# # def archive_patient_visit(request, vis_id):
# #     """ Archive patient visit"""
# #
# #     visit = get_object_or_404(PatientVisit, pk=vis_id)
# #
# #         # --- NEW VALIDATION LOGIC ---
# #     open_post_actions = []
# #     if PatientLab.objects.filter(visit_title=visit, closed=False).exists():
# #         open_post_actions.append('Labs')
# #     if DentistReport.objects.filter(visit_title=visit, closed=False).exists():
# #         open_post_actions.append('Reports')
# #     if PatientReferral.objects.filter(visit_title=visit, closed=False).exists():
# #         open_post_actions.append('Referrals')
# #     if PatientTreatment.objects.filter(visit_title=visit, closed=False).exists():
# #         open_post_actions.append('Treatments')
# #
# #     if open_post_actions:
# #         messages.error(request, 'Patient visit has open items')
# #         return redirect(request.path)
# #
# #     if request.method == 'POST':
# #         try:
# #             # Pass the object, not just ID
# #             perform_archive_tasks(visit.id)
# #             messages.success(request, 'Visit closed and archived successfully.')
# #             return redirect('patients:listallpatientvisits') # Redirect away
# #         except ValidationError as e:
# #             messages.error(request, f'Error: {e}')
# #             return redirect(request.path)
# #     return render(request, 'patients/archive_patient_visit.html', {'h_visit': visit})
#
#
# # View archived visit
# @login_required
# @role_required(allowed_roles=['Employee', 'Dentist', 'Admin', 'Patient'])
# def view_archived_visit(request, vis_id):
#
#     archived_visit = get_object_or_404(ArchivedPatientVisit, pk=vis_id)
#     form = ArchivedPatientVisitForm(instance=archived_visit)
#
#     for field in form.fields.values():
#         field.disabled = True
#
#     context = {
#         'h_form': form,
#         'h_archivedvisit': archived_visit
#     }
#     return render(request, 'patients/view_archived_visit.html', context)
#
#
# # View patient bill
# @login_required
# @role_required(allowed_roles=['Employee', 'Dentist', 'Admin'])
# def view_visitcost(request, vis_id):
#     """ Read only view for current charges for dental services """
#
#     visit = PatientVisit.objects.get(pk=vis_id)
#     total_cost = visit.services.aggregate(total_sum=Sum('price'))['total_sum']
#
#     context = {
#         'h_visit': visit,
#         'h_totalcost': total_cost
#     }
#     return render(request,'patients/patient_visitcost.html', context)
#
#
# # List all visits
# @login_required
# @role_required(allowed_roles=['Employee', 'Dentist', 'Admin'])
# def list_all_patient_visits(request):
#     """ List visits for all patients """
#     today = date.today()
#
#     query = request.GET.get('item_name')
#     allvisits = PatientVisit.objects.order_by('visit_date')
#
#     if query:
#         allvisits = allvisits.filter(
#             Q(visit_title__icontains=query) |
#             Q(patient__last_name__icontains=query) |
#             Q(patient__first_name__icontains=query)
#         ).distinct()
#     else:
#         allvisits = PatientVisit.objects.all().order_by('visit_date')
#
#     paginator = Paginator(allvisits, per_page=10)
#     page_number = request.GET.get('page')
#     page_allvisits = paginator.get_page(page_number)
#
#     context = {
#         'h_today': today,
#         'page_allvisits': page_allvisits,
#         'h_visitstotal': allvisits.count(),
#     }
#     return render(request, 'patients/list_patientvisits.html', context)
#
#
# # List patient visits
# @login_required
# @role_required(allowed_roles=['Employee', 'Dentist', 'Admin'])
# def list_patient_visits(request, pat_id):
#     """ List visits for a patient """
#
#     patient = get_object_or_404(Patient, pk=pat_id)
#     patient_visits = PatientVisit.objects.filter(patient=patient)
#     context = {
#         'h_patient': patient,
#         'h_patientvisits': patient_visits
#     }
#     return render(request, 'patients/patient_visits_one_patient.html', context)
#
#
# # Delete visit
# @login_required
# @role_required(allowed_roles=['Dentist', 'Admin', 'Employee'])
# def delete_patient_visit(request, vis_id):
#
#     visit = PatientVisit.objects.get(pk=vis_id)
#
#     if request.method == 'POST':
#         visit.delete()
#         messages.success(request, 'Patient visit deleted!')
#         return redirect('patients:listallpatientvisits')
#     context = {
#         'h_visit': visit
#     }
#     return render(request, context)
