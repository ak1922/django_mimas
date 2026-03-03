from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import AccountUser
from accounts.decorators import group_required
from mimascompany.models.employee_model import Employee
from mimascompany.models.leaverequests_model import LeaveRequest
from mimascompany.forms.employeeleave_form import LeaveRequestForm


# Create request
@login_required
@group_required(allowed_groups=['Employees', 'Administrators'])
def create_leave_request(request):

    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            new_request = form.save()
            messages.success(request, f'New request created for {new_request.employee.full_name}')
            return redirect('mimascompany:listallleaverequests')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}:- {error}')
    else:
        form = LeaveRequestForm()

    context = {
        'h_form': form,
        'h_exists_request': None
    }
    return render(request, 'mimascompany/create_leaverequest.html', context)


# List requests
@login_required
@group_required(allowed_groups=['Employees', 'Administrators'])
def list_all_leaverequests(request):

    query = request.GET.get('item_name')
    all_requests = LeaveRequest.objects.all().order_by('start_date')

    if query:
        all_requests = all_requests.filter(
            Q(employee__last_name__icontains=query) |
            Q(employee__first_name__icontains=query) |
            Q(employee__user__username__icontains=query) |
            Q(approved_by__employee_accountuser__first_name__icontains=query) |
            Q(approved_by__employee_accountuser__last_name__icontains=query)
        ).distinct()
    else:
        all_requests = LeaveRequest.objects.all().order_by('start_date')

    paginator = Paginator(all_requests, per_page=5)
    page_number = request.GET.get('page')
    page_allrequests = paginator.get_page(page_number)

    context = {
        'page_allrequests': page_allrequests,
        'h_allrequestscount': all_requests.count()
    }
    return render(request, 'mimascompany/list_leaverequests.html', context)


# Edit requests
@login_required
@group_required(allowed_groups=['Employees', 'Administrators'])
def edit_leave_request(request, req_id):

    employee_request = get_object_or_404(LeaveRequest, pk=req_id)

    if request.method == 'POST':
        form = LeaveRequestForm(request.POST, instance=employee_request)
        if form.is_valid():
            current_user = get_object_or_404(AccountUser, username=request.user)
            edited_request = form.save(commit=False)
            edited_request.updated_by = current_user
            edited_request.save()
            messages.success(request, f'Leave request updated for {edited_request.employee.full_name}.')
            return redirect('mimascompany:listallleaverequests')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}:- {error}')
    else:
        form = LeaveRequestForm(instance=employee_request)
    return render(request, 'mimascompany/create_leaverequest.html', {'h_form': form})


# View leave request
@login_required
@group_required(allowed_groups=['Employees', 'Administrators'])
def view_leave_request(request, req_id):

    employee_request = get_object_or_404(LeaveRequest, pk=req_id)
    form = LeaveRequestForm(instance=employee_request)

    for field in form.fields.values():
        field.disabled = True

    context = {
        'h_form': form,
        'h_exists_request': employee_request
    }
    return render(request, 'mimascompany/create_leaverequest.html', context)


# Delete request
@login_required
@group_required(allowed_groups=['Employees', 'Administrators'])
def delete_leave_request(request, req_id):

    employee_request = get_object_or_404(LeaveRequest, pk=req_id)
    employee = Employee.objects.get(user=employee_request.employee.user)

    if request.method == 'POST':
        employee_request.delete()
        messages.success(request, f'Leave request deleted for {employee.full_name}')
    return redirect('mimascompany:listallleaverequests')
