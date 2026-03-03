from django.db.models import Q
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import AccountUser
from accounts.decorators import group_required
from mimascompany.models.employee_model import Employee
from mimascompany.models.employeecontact_model import EmployeeContact
from mimascompany.forms.employeecontact_form import EmployeeContactForm


# Create employee contact no table
@login_required
@group_required(allowed_groups=['Dentists', 'Employees', 'Administrators'])
def create_employee_contact(request):

    if request.method == 'POST':
        form = EmployeeContactForm(request.POST)
        if form.is_valid():
            new_contact = form.save()
            messages.success(request, f'New contact created for {new_contact.employee_name}')
            return redirect('mimascompany:listemployeecontacts')
        else:
            messages.error(request, 'Invalid form.')
    else:
        form = EmployeeContactForm()

    context = {
        'h_form': form,
        'h_exists_contact': None
    }
    return render(request,'mimascompany/create_employeecontact.html', context)


# Create contact from employees
@login_required
@group_required(allowed_groups=['Dentists', 'Employees', 'Administrators'])
def add_employee_contact_employee(request, emp_id=None):
    """ Add employee contact from employee table list """


    employee_contact = None
    if emp_id:
        employee = get_object_or_404(Employee, pk=emp_id)

        try:
            employee_contact = employee.employeecontact_employee
        except EmployeeContact.DoesNotExist:
            employee_contact = EmployeeContact(employee=employee)

    if request.method == 'POST':
        form = EmployeeContactForm(request.POST, instance=employee_contact)

        if form.is_valid():
            new_contact = form.save()
            messages.success(request, f'New contact created for {new_contact.employee_name}')
            return redirect('mimascompany:listemployees')
        else:
            messages.error(request, 'Invalid form.')

    else:
        form = EmployeeContactForm(instance=employee_contact)
    return render(request,'mimascompany/create_employeecontact.html', {'h_form': form})


# Edit employee contect
@login_required
@group_required(allowed_groups=['Dentists', 'Employees', 'Administrators'])
def edit_employee_contact(request, con_id):

    contact = get_object_or_404(EmployeeContact, pk=con_id)
    if request.method == 'POST':
        form = EmployeeContactForm(request.POST, instance=contact)

        if form.is_valid():
            current_user = AccountUser.objects.get(username=request.user)
            edited_contact = form.save(commit=False)
            edited_contact.updated_by = current_user
            edited_contact.save()
            messages.success(request, f'Contact information for {edited_contact.employee_name} updated.')
            return redirect('mimascompany:listemployeecontacts')
        else:
            messages.error(request, 'Issues with form update for employee contact information.')

    else:
        form = EmployeeContactForm(instance=contact)

    context = {
        'h_form': form,
        'h_contact': contact,
    }
    return render(request,'mimascompany/create_employeecontact.html', context)


# List contacts
@login_required
@group_required(allowed_groups=['Dentists', 'Employees', 'Administrators'])
def list_employee_contacts(request):

    query = request.GET.get('item_name')
    employeescount = Employee.objects.all().count()
    allcontacts = EmployeeContact.objects.all().order_by('created')

    # Search
    if query:
        allcontacts = allcontacts.filter(
            Q(contact_name__icontains=query) |
            Q(employee__last_name__icontains=query) |
            Q(employee__first_name__icontains=query)
        ).distinct()
    else:
        allcontacts = EmployeeContact.objects.all().order_by('created')

    # Pagination
    paginator = Paginator(allcontacts, per_page=5)
    page_number = request.GET.get('page')
    page_allcontacts = paginator.get_page(page_number)

    context = {
        'h_query': query,
        'h_employeescount': employeescount,
        'page_allcontacts': page_allcontacts,
        'h_contactscount': allcontacts.count(),
    }
    return render(request, 'mimascompany/list_employeecontacts.html', context)

# View contact
@login_required
@group_required(allowed_groups=['Dentists', 'Employees', 'Administrators'])
def view_employee_contact(request, con_id):

    contact = EmployeeContact.objects.get(pk=con_id)
    form = EmployeeContactForm(instance=contact)

    for field in form.fields.values():
        field.disabled = True

    context = {
        'h_form': form,
        'h_exists_contact': contact
    }
    return render(request, 'mimascompany/create_employeecontact.html', context)


# Delete contact
@login_required
@group_required(allowed_groups=['Dentists', 'Employees', 'Administrators'])
def delete_employee_contact(request, con_id):

    contact = EmployeeContact.objects.get(pk=con_id)

    if request.method == 'POST':
        contact.delete()
        messages.success(request, 'Contact information deleted')
    return redirect('mimascompany:listemployeecontacts')
