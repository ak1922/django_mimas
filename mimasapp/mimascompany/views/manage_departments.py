from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import group_required
from accounts.models import AccountUser
from mimascompany.models.department_model import Department
from mimascompany.forms.company_forms import DepartmentForm


# Create department
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def create_department(request):
    """ Create department """

    if request.method == 'POST':
        form = DepartmentForm(request.POST)

        if form.is_valid():
            new_dept = form.save()
            messages.success(request, f'New department {new_dept.department_name} created.')
            return redirect('mimascompany:listdepartments')
        else:
            messages.error(request, 'Issues with department creation!')

    else:
        form = DepartmentForm()
    return render(request, 'mimascompany/create_department.html', {'h_form': form})


# Edit department
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def edit_department(request, dept_id):

    department = Department.objects.get(pk=dept_id)

    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)

        if form.is_valid():
            current_user = AccountUser.objects.get(username=request.user)
            edited_department = form.save(commit=False)
            edited_department.updated_by = current_user
            edited_department.save()
            messages.success(request, f'Department {edited_department.department_name} updated!')
            return redirect('mimascompany:listdepartments')
        else:
            messages.error(request, 'Issues with department update!')

    else:
        form = DepartmentForm(instance=department)
    return render(request, 'mimascompany/create_department.html', {'h_form': form})


# List departments
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def list_departments(request):

    query = request.GET.get('item_name')
    alldepartments = Department.objects.all().order_by('created')

    if query:
        alldepartments = alldepartments.filter(
            Q(department_name__icontains=query) |
            Q(department_head__last_name__icontains=query) |
            Q(department_head__first_name__icontains=query)
        ).distinct()
    else:
        alldepartments = Department.objects.all().order_by('created')

    paginator = Paginator(alldepartments, per_page=5)
    page_number = request.GET.get('page')
    page_alldepartments = paginator.get_page(page_number)

    context = {
        'page_alldepartments': page_alldepartments,
        'h_departmentstotal': alldepartments.count()
    }
    return render(request, 'mimascompany/list_departments.html', context)


# Department read only
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def view_department(request, dept_id):

    department = get_object_or_404(Department, pk=dept_id)
    form = DepartmentForm(instance=department)

    for field in form.fields.values():
        field.disabled = True

    context = {
        'h_form': form,
        'h_department': department
    }
    return render(request, 'mimascompany/create_department.html', context)


# Delate department
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def delete_department(request, dept_id):

    department = Department.objects.get(pk=dept_id)
    if request.method == 'POST':
        department.delete()
    return redirect('mimascompany:listdepartments')
