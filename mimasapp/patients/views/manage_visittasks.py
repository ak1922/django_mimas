import logging
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from accounts.decorators import group_required
from mimascompany.models.employee_model import Employee
from patients.models.patientvisit_models import PatientVisit
from patients.models.visittask_model import PatientVisitTask
from patients.forms.visittask_forms import PatientVisitTaskForm


logger = logging.getLogger(__name__)


# Create ad-hoc visit task
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators', 'Employees'])
def create_visit_task(request):

    next_url = request.GET.get('next', reverse('patients:listvisittasks'))

    if request.method == 'POST':
        form = PatientVisitTaskForm(request.POST)
        if form.is_valid():
            task_owner = Employee.active_employees.get(user=request.user)
            new_task = form.save(commit=False)
            new_task.assigned_to = task_owner
            new_task.save()
            messages.success(request, f'New visit task {new_task.task_title} created.')
            logger.info(f'New visit task {new_task.task_title} created by {request.user}')
            return redirect(next_url)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field} - {error}')
                    logger.error(f'{field} - {error}')
    else:
        form = PatientVisitTaskForm()

    context = {
        'h_form': form,
        'h_exists_task': None
    }
    return render(request, 'patients/create_visittask.html', context)


# Create visit task from visit
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators', 'Employees'])
def create_visit_task_visit(request, vis_id):

    next_url = request.GET.get('next', reverse('patients:listvisittasks'))
    patient_visit = get_object_or_404(PatientVisit, pk=vis_id)

    if request.method == 'POST':
        form = PatientVisitTaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.visit = patient_visit
            new_task.save()
            messages.success(request, f'New visit task created for {patient_visit.visit_title}.')
            logger.info(f'New visit task created for {patient_visit.visit_title} create by {request.user}.')
            return redirect(next_url)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field} - {error}')
                    logger.error(f'{field} - {error}')
    else:
        form = PatientVisitTaskForm(initial={
            'appointment': patient_visit.appointment,
            'visit': patient_visit
        })
    context = {
        'h_form': form,
        'h_exists_task': None
    }
    return render(request, 'patients/create_visittask.html', context)


# Edit visit task
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators', 'Employees'])
def edit_visit_task(request, task_id):

    visit_task = get_object_or_404(PatientVisitTask, pk=task_id)

    if request.method == 'POST':
        form = PatientVisitTaskForm(request.POST, instance=visit_task)
        if form.is_valid():
            current_user = get_object_or_404(Employee, user=request.user)
            new_task = form.save(commit=False)
            new_task.updated_by = current_user
            new_task.save()
            messages.success(request, f'Visit task {new_task.task_title} updated.')
            logger.info(f'Visit task {new_task.task_title} updated by {request.user}.')
            return redirect('patients:listvisittasks')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field} - {error}')
                    logger.error(f'{field} - {error}')
    else:
        form = PatientVisitTaskForm(instance=visit_task)
    return render(request, 'patients/create_visittask.html', {'h_form': form})


# View task
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators', 'Employees'])
def view_visit_task(request, task_id):

    visit_task = get_object_or_404(PatientVisitTask, pk=task_id)
    form = PatientVisitTaskForm(instance=visit_task)

    for field in form.fields.values():
        field.disabled = True

    context = {
        'h_form': form,
        'h_exists_task': visit_task
    }
    return render(request, 'patients/create_visittask.html', context)


# List visit tasks
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators', 'Employees'])
def list_visit_task(request):

    query = request.GET.get('item_name')
    allvisit_tasks = PatientVisitTask.objects.all().order_by('-created')

    if query:
        allvisit_tasks = allvisit_tasks.filter(
            Q(task_title__icontains=query)
        ).distinct()
    else:
        allvisit_tasks = PatientVisitTask.objects.all().order_by('-created')

    context = {
        'h_allvisittasks': allvisit_tasks,
        'h_alltaskstotal': allvisit_tasks.count()
    }
    return render(request, 'patients/list_visittasks.html', context)


# Delete task
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators', 'Employees'])
def delete_visit_task(request, task_id):

    visit_task = get_object_or_404(PatientVisitTask, pk=task_id)
    if request.method == 'POST':
        visit_task.delete()
    return redirect('patients:listvisittasks')
