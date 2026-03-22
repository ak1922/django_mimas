import logging
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import AccountUser
from accounts.decorators import group_required
from mimascompany.forms import ServiceForm
from mimascompany.models import Service, Department


logger = logging.getLogger(__name__)


# Create service
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def create_service(request):

    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            new_service = form.save()
            messages.success(request, f'New service {new_service} created for {new_service.department} department by {request.user}.')
            logger.info(f'New service {new_service} created for {new_service.department} department by {request.user}.')
            return redirect('mimascompany:listservices')
        else:
            for error in form.errors.items():
                messages.error(request, f'Service Form:- {error}')
                logger.error(f'Service Form:- {error}')
    else:
        form = ServiceForm()
    context = {
        'h_form': form,
        'h_exists_service': None
    }
    return render(request, 'mimascompany/create_service.html', context)


# Add service from departments
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def create_service_with_department(request, dept_id):

    department = get_object_or_404(Department, pk=dept_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if request.method == 'POST':
            new_service = form.save(commit=False)
            new_service.department = department
            new_service.save()
            messages.success(request, f'New service added to {new_service.department}')
            logger.info(f'New service added to {new_service.department} by {request.user}')
            return redirect('mimascompany:listdepartments')
        else:
            for error in form.errors.items():
                messages.error(request, f'Service Form:- {error}')
                logger.error(f'Service Form:- {error}')
    else:
        form = ServiceForm(initial={
            'department': department
        })
    return render(request, 'mimascompany/create_service.html', {'h_form': form})


# List all services
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def list_services(request):
    """ List all dental services """

    allservices = Service.objects.all().order_by('-created')
    query = request.GET.get('item_name')

    if query:
        allservices = allservices.filter(
            Q(service_name__icontains=query) |
            Q(department__department_name__icontains=query)
        ).distinct()
    else:
        allservices = Service.objects.all().order_by('-created')

    # Add pagination
    paginator = Paginator(allservices, per_page=10)
    page_number = request.GET.get('page')
    page_services = paginator.get_page(page_number)

    context = {
        'page_services': page_services,
        'h_servicescount': allservices.count()
    }
    return render(request, 'mimascompany/list_services.html', context)


# Edit service
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def edit_service(request, svc_id):

    service = Service.objects.get(pk=svc_id)

    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)

        if form.is_valid():
            current_user = AccountUser.objects.get(username=request.user)
            edited_service = form.save(commit=False)
            edited_service.updated_by = current_user
            edited_service.save()
            messages.success(request, f'Service {edited_service.service_name} updated by {request.user}.')
            return redirect('mimascompany:listservices')
        else:
            messages.error(request, 'Issues updating dental service.')

    else:
        form = ServiceForm(instance=service)
    return render(request, 'mimascompany/create_service.html', {'h_form': form})


# View service
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def view_service(request, svc_id):

    service = get_object_or_404(Service, pk=svc_id)
    form = ServiceForm(instance=service)

    for field in form.fields.values():
        field.disabled = True

    context = {
        'h_form': form,
        'h_exists_service': service
    }
    return render(request, 'mimascompany/create_service.html', context)


# Delete service
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def delete_service(request, svc_id):

    service = Service.objects.get(pk=svc_id)
    if request.method == 'POST':
        service.delete()
    return redirect('mimascompany:listservices')
