import logging
from PIL import Image
from django.db import transaction
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from accounts.models import AccountUser
from accounts.forms import RegisterAppUserForm
from accounts.decorators import group_required
from mimascompany.models.employee_model import Employee
from mimascompany.forms.employee_form import EmployeeForm


# Set up logging
logger = logging.getLogger(__name__)


# Create employee view
class EmployeeCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):

    model = Employee
    form_class = EmployeeForm
    template_name = 'mimascompany/create_employee.html'
    success_url = reverse_lazy('mimascompany:listemployees')
    success_message = 'New employee, %(first_name)s %(last_name)s, created successfully.'

    def test_func(self):
        """Restrict access to Administrators or Employees."""
        allowed_groups = ['Administrators', 'Employees']
        return self.request.user.groups.filter(name__in=allowed_groups).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['h_form'] = context['form']
        return context

    def form_valid(self, form):
        form.instance.create_by = self.request.user
        with transaction.atomic():
            response = super().form_valid(form)
            employee = form.instance
            logger.info(
                f'Employee created: {employee.first_name} {employee.last_name}'
                f'Created by: {self.request.user}'
            )
            return response

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'{field}:- {error}')
        return super().form_invalid(form)


# List employees
@login_required
@group_required(allowed_groups=['Administrators', 'Employees'])
def list_employees(request):

    all_employees = Employee.objects.all()

    paginator = Paginator(all_employees, 10)
    page_number = request.GET.get('page')
    page_allemployees = paginator.get_page(page_number)

    context = {
        'page_allemployees': page_allemployees,
        'h_allemployeescount': all_employees.count()
    }
    return render(request, 'mimascompany/list_employees.html', context)


# Edit employee
@login_required
@group_required(allowed_groups=['Administrators', 'Employees'])
def edit_employee(request, emp_id):

    employee = get_object_or_404(Employee, pk=emp_id)
    user = employee.user

    if request.method == 'POST':
        form_a = EmployeeForm(request.POST, request.FILES, instance=employee)
        form_b = RegisterAppUserForm(request.POST, instance=user)

        if form_a.is_valid() and form_b.is_valid():
            try:
                with transaction.atomic():
                    current_user = get_object_or_404(AccountUser, username=request.user)

                    # ---- RegistrationForm Intake -----
                    user_instance = form_b.save(commit=False)
                    password = form_b.cleaned_data.get('password1')
                    if password:
                        user_instance.set_password(password)
                    user_instance.save()

                    # ---- EmployeeForm Intake -----
                    employee_instance = form_a.save(commit=False)
                    employee_instance.updated_by = current_user
                    # ---- Check for employee photo ----
                    if 'photo' in request.FILES:
                        img = Image.open(employee_instance.photo.path)
                        output_size = (300, 300)
                        img = img.resize(output_size, Image.Resampling.LANCZOS)
                        img.save(employee_instance.photo.path)
                    # ---- Finally EmployeeForm
                    employee_instance.save()

                # ---- Messages and Logging ----
                messages.success(request, f'Information for {employee.full_name} updated.')
                logger.info(f'Information for {employee.full_name} updated.')
                return redirect('mimascompany:listemployees')

            except Exception as e:
                messages.error(request, f'Error updating employee: {e}')
        else:
            for field, errors in form_a.errors.items():
                messages.error(request, f'Employee Form - {field}: {errors[0]}')
            for field, errors in form_b.errors.items():
                messages.error(request, f'User Form - {field}: {errors[0]}')
    else:
        form_a = EmployeeForm(instance=employee)
        form_b = RegisterAppUserForm(instance=user)
        # Set password field empty
        form_b.fields['password1'].required = False
        form_b.fields['password2'].required = False

    context = {
        'h_forma': form_a,
        'h_formb': form_b,
        'h_employee': employee
    }
    return render(request, 'mimascompany/edit_employee.html', context)


# Delete employee
@login_required
def delete_employee(request, emp_id):

    employee = get_object_or_404(Employee, pk=emp_id)
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employee deleted')
        logger.info(request, 'Employee deleted')
    return redirect('mimascompany:listemployees')
