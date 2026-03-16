import logging
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from mimascompany.models import Employee
from accounts.decorators import group_required
from patients.forms import PatientBillForm, ArchivedPatientBillReadOnlyForm
from patients.models import PatientBill, ArchivedPatientBill, PatientVisit


logger = logging.getLogger(__name__)

# Edit patient bill
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def pay_patient_bill(request, bill_id):

    bill = get_object_or_404(PatientBill, pk=bill_id)

    try:
        visit = PatientVisit.objects.get(visit_title=bill.visit)
    except PatientVisit.DoesNotExist:
        messages.error(request, 'Associated visit not found.')
        return redirect('patients:listallbills')

    if request.method == 'POST':

        form = PatientBillForm(request.POST, instance=bill)
        if form.is_valid():
            current_user = get_object_or_404(Employee, user=request.user)
            new_bill = form.save(commit=False)
            new_bill.updated_by = current_user
            new_bill.save()

            if bill.is_paid:
                visit.visit_status = 'Closed'
                visit.save()
                messages.success(request, f'{bill} bill paid for patient visit! Visit status set to Closed.')
                logger.info(f'{bill} bill paid for patient visit! Visit status set to Closed.')
            return redirect('patients:listallbills')
        else:
            messages.error(request, 'Invalid patient bill submitted')
    else:
        form = PatientBillForm(instance=bill)

    context = {
        'h_form': form,
        'h_paybill': bill
    }
    return render(request, 'patients/patient_bill.html', context)


# View patient bill
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def view_patient_bill(request, bill_id):
    """ Read only view for current patient bill """

    bill = PatientBill.objects.get(pk=bill_id)
    form = PatientBillForm(instance=bill)

    for field in form.fields.values():
        field.disabled = True

    context = {
        'h_form': form,
        'h_paybill': None
    }
    return render(request, 'patients/patient_bill.html', context)


# List patient bills
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def list_all_bills(request):
    """ List of current patients bills """

    query = request.GET.get('item_name')
    allbills = PatientBill.objects.all().order_by('created')

    if query:
        allbills = allbills.filter(
            Q(bill_title__icontains=query) |
            Q(patient__first_name__icontains=query) |
            Q(patient__last_name__icontains=query)
        ).distinct()
    else:
        allbills = PatientBill.objects.all().order_by('created')

    paginator = Paginator(allbills, per_page=10)
    page_number = request.GET.get('page')
    page_allbills = paginator.get_page(page_number)

    context = {
        'page_allbills': page_allbills,
        'h_allbillscount': allbills.count()
    }
    return render(request, 'patients/list_bills.html', context)



#------------------ Archived bills --------------------

# View archived bill
@login_required
def view_archived_bill(request, bill_id):

    archived_bill = ArchivedPatientBill.objects.get(pk=bill_id)
    form = ArchivedPatientBillReadOnlyForm(instance=archived_bill)

    for field in form.fields.values():
        field.disabled = True

    context = {
        'h_form': form,
        'h_archivedbill': archived_bill
    }
    return render(request, 'patients/view_archivedbill.html', context)


# Archived bills
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def list_archived_bills(request):

    query = request.GET.get('item_name')
    allarchivedbills = ArchivedPatientBill.objects.all().order_by('archived')

    if query:
        allarchivedbills = allarchivedbills.filter(
            Q(bill_title__icontains=query) |
            Q(patient__icontains=query)
        ).distinct()
    else:
        allarchivedbills = ArchivedPatientBill.objects.all().order_by('archived')

    paginator = Paginator(allarchivedbills, per_page=10)
    page_number = request.GET.get('page')
    page_archivedbills = paginator.get_page(page_number)

    context = {
        'page_archivedbills': page_archivedbills,
        'h_archivedcount': allarchivedbills.count(),
    }
    return render(request, 'patients/list_archivedbills.html', context)
