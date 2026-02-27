from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import AccountUser
from accounts.decorators import group_required
from mimascompany.models.dentist_model import Dentist
from mimascompany.models.employee_model import Employee
from mimascompany.forms.dentists_froms import DentistForm
from mimascompany.forms.employee_form import EmployeeForm


# Create dentist
@login_required
@group_required(allowed_groups=['Employees', 'Dentists', 'Administrators'])
def create_dentist(request):

    if request.method == 'POST':
        form = DentistForm(request.POST)

        if form.is_valid():
            new_dentist = form.save()
            messages.success(request, f'New dentist created for {new_dentist.dentist_name}')
            return redirect('mimascompany:listdentists')
        else:
            messages.error(request, 'Issues encounted creating new dentist.')

    else:
        form = DentistForm()
    return render(request, 'mimascompany/create_dentist.html', {'h_form': form})


# Update dentist employee info
@login_required
@group_required(allowed_groups=['Employees', 'Dentists', 'Administrators'])
def update_info_dentist_dash(request, emp_id=None):
    """ Update dentist employee information from dentist dashboard """

    dentist = None
    if emp_id:
        try:
            dentist = get_object_or_404(Employee, pk=emp_id)
        except Employee.DoesNotExist:
            dentist = Employee(user=dentist)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=dentist)

        if form.is_valid():
            dentist_info = form.save()
            messages.success(request, f'Employee information for {dentist_info.first_name} {dentist_info.last_name}')
            # return redirect('dentists:dentistdashboard', emp_id)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Employee Form Error:- {field}: {error}')
            # Generic message
            messages.error(request, 'Form validation issues')

    else:
        form = EmployeeForm(instance=dentist)
    return render(request, 'mimascompany/create_employee.html', {'h_form': form})


# Edit dentist
@login_required
@group_required(allowed_groups=['Employees', 'Dentists', 'Administrators'])
def edit_dentist(request, den_id):

    dentist = Dentist.objects.get(pk=den_id)

    if request.method == 'POST':
        form = DentistForm(request.POST, instance=dentist)

        if form.is_valid():
            current_user = AccountUser.objects.get(username=request.user)
            edited_dentist = form.save(commit=False)
            edited_dentist.updated_by = current_user
            edited_dentist.save()
            messages.success(request, f'Information for {edited_dentist.dentist_name} updated.')
            return redirect('mimascompany:listdentists')
        else:
            messages.error(request, 'Issues encounted updating dentist information.')
    else:
        form = DentistForm(instance=dentist)
    return render(request, 'mimascompany/create_dentist.html', {'h_form': form})


# List dentists
@login_required
@group_required(allowed_groups=['Employees', 'Dentists', 'Administrators'])
def list_dentists(request):

    query  = request.GET.get('item_name')
    alldentists = Dentist.objects.all().order_by('created')

    if query:
        alldentists = alldentists.filter(
            Q(employee__first_name__icontains=query) |
            Q(employee__last_name__icontains=query)
        ).distinct()
    else:
        alldentists = Dentist.objects.all().order_by('created')

    paginator = Paginator(alldentists, per_page=5)
    page_number = request.GET.get('page')
    page_alldentists = paginator.get_page(page_number)

    context = {
        'page_alldentists': page_alldentists,
        'h_alldentistscount': alldentists.count()
    }
    return render(request, 'mimascompany/list_dentists.html', context)


# Delete dentist
@login_required
@group_required(allowed_groups=['Employees', 'Dentists', 'Administrators'])
def delete_dentist(request, den_id):

    dentist = Dentist.objects.get(pk=den_id)
    if request.method == 'POST':
        dentist.delete()
        messages.success(request, 'Dentist deleted.')
    return redirect('mimascompany:listdentists')
