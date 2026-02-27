from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import AccountUser
from accounts.decorators import group_required
from mimascompany.models.employee_model import Employee
from mimascompany.models.employeedetails_model import EmployeeDetail
from mimascompany.forms.employeedetail_form import EmployeeDetailForm


# Create employee detail record
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def create_employee_detail(request):
    """ Create detail for employee """

    if request.method == 'POST':
        form = EmployeeDetailForm(request.POST)

        if form.is_valid():
            new_detail = form.save()
            messages.success(request, f'New employee detail added for {new_detail.employee.full_name}')
            return redirect('mimascompany:listemployeedetails')
        else:
            messages.error(request, 'Issues with creating employee detail.')

    else:
        form = EmployeeDetailForm()
    return render(request,'mimascompany/create_employeedetail.html', {'h_form': form})


# # Create employee details with table
# @login_required
# @role_required(allowed_roles=['Employee', 'Admin'])
# def create_employeedetail_with_table(request):
#
#     alldetails = EmployeeDetail.objects.all().order_by('-modified_on')
#     allemployees = Employee.objects.all().count()
#
#     paginator = Paginator(alldetails, per_page=4)
#     page_number = request.GET.get('page')
#     page_alldetails = paginator.get_page(page_number)
#
#     if request.method == 'POST':
#         form = EmployeeDetailForm(request.POST)
#
#         if form.is_valid:
#             new_detail = form.save()
#             messages.success(request, f'New employee detail added for {new_detail.employee.full_name}')
#             return redirect(request.path)
#         else:
#             messages.error(request, 'Invalid form.')
#
#     else:
#         form = EmployeeDetailForm()
#
#     context = {
#         'h_form': form,
#         'h_allemployees': allemployees,
#         'page_alldetails': page_alldetails,
#         'h_detailstotal': alldetails.count(),
#     }
#     return render(request,'marscompany/create_employeedetails_table.html', context)


# Add employee detail form employee
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def create_employee_detail_employee(request, emp_id=None):

    employee_detail = None
    if emp_id:
        employee = get_object_or_404(Employee, pk=emp_id)

        try:
            employee_detail = employee.employeedetail_employee
        except EmployeeDetail.DoesNotExist:
            employee_detail = EmployeeDetail(employee=employee)

    if request.method == 'POST':
        form = EmployeeDetailForm(request.POST, instance=employee_detail)

        if form.is_valid():
            new_detail = form.save()
            messages.success(request, f'New employee detail added for {new_detail.employee.full_name}')
            return redirect('mimascompany:listemployeedetails')
        else:
            messages.error(request, 'Invalid form submitted!')

    else:
        form = EmployeeDetailForm(instance=employee_detail)
    return render(request,'mimascompany/create_employeedetail.html', {'h_form': form})


# Edit employee detail record
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def edit_employee_detail(request, det_id):
    """ Edit detail record for employee """

    detail = EmployeeDetail.objects.get(pk=det_id)

    if request.method == 'POST':
        form = EmployeeDetailForm(request.POST, instance=detail)

        if form.is_valid():
            current_user = AccountUser.objects.get(username=request.user)
            edited_detail = form.save(commit=False)
            edited_detail.updated_by = current_user
            edited_detail.save()
            messages.success(request, f'Details for employee {edited_detail.employee.full_name} updated.')
            return redirect('mimascompany:listemployeedetails')
        else:
            messages.error(request, 'Issues updating employee details')

    else:
        form = EmployeeDetailForm(instance=detail)
    return render(request,'mimascompany/create_employeedetail.html', {'h_form': form})


# List employee details
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def list_employee_details(request):
    """ List detaild record for employees """

    allemployees = Employee.objects.all().count()
    allemployeedetails = EmployeeDetail.objects.all().order_by('created')
    query = request.GET.get('item_name')

    if query:
        allemployeedetails = allemployeedetails.filter(
            Q(employee__first_name__icontains=query) |
            Q(employee__last_name__icontains=query)
        ).distinct()
    else:
        allemployeedetails = EmployeeDetail.objects.all().order_by('created')

    paginator = Paginator(allemployeedetails, per_page=5)
    page_number = request.GET.get('page')
    page_details = paginator.get_page(page_number)

    context = {
        'page_details': page_details,
        'h_allemployees': allemployees,
        'h_destailscount': allemployeedetails.count()
    }
    return render(request, 'mimascompany/list_employeedetails.html', context)


# # Read only employee detail
# @login_required
# @group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
# def view_employee_detail(request, det_id):
#     """ Read only view for employee detail record """
#
#     detail = EmployeeDetail.objects.get(pk=det_id)
#     form = EmployeeDetailFormReadOnly(instance=detail)
#
#     for field in form.fields.values():
#         field.disabled = True
#
#     context = {
#         'h_form': form,
#         'h_detail': detail
#     }
#     return render(request, 'marscompany/view_employeedetails.html', context)


# Delete employee detail
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def delete_employee_detail(request, det_id):
    """ Delete detail record for employee including dentists and managers """

    detail = EmployeeDetail.objects.get(pk=det_id)
    if request.method == 'POST':
        detail.delete()
    return redirect('mimascompany:listemployeedetails')
