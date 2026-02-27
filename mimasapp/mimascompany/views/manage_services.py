from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import AccountUser
from accounts.decorators import group_required
from mimascompany.models.service_model import Service
from mimascompany.forms.company_forms import ServiceForm


# List services
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employee'])
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
    paginator = Paginator(allservices, per_page=5)
    page_number = request.GET.get('page')
    page_services = paginator.get_page(page_number)

    context = {
        'page_services': page_services,
        'h_servicescount': allservices.count()
    }
    return render(request, 'mimascompany/list_services.html', context)


# Create service
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employee'])
def create_service(request):

    if request.method == 'POST':
        form = ServiceForm(request.POST)

        if form.is_valid():
            new_service = form.save()
            messages.success(request, f'New service {new_service} created for {new_service.department}.')
            return redirect('mimascompany:listservices')
        else:
            messages.error(request, 'Issues creating new service.')

    else:
        form = ServiceForm()
    return render(request, 'mimascompany/create_service.html', {'h_form': form})


# Edit service
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employee'])
def edit_service(request, svc_id):

    service = Service.objects.get(pk=svc_id)

    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)

        if form.is_valid():
            current_user = AccountUser.objects.get(username=request.user)
            edited_service = form.save(commit=False)
            edited_service.updated_by = current_user
            edited_service.save()
            messages.success(request, f'Service {edited_service.service_name} updated.')
            return redirect('mimascompany:listservices')
        else:
            messages.error(request, 'Issues updating dental service.')

    else:
        form = ServiceForm(instance=service)
    return render(request, 'mimascompany/create_service.html', {'h_form': form})


# Delete service
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employee'])
def delete_service(request, svc_id):

    service = Service.objects.get(pk=svc_id)
    if request.method == 'POST':
        service.delete()
    return redirect('mimascompany:listservices')


# View service
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employee'])
def view_service(request, svc_id):

    service = get_object_or_404(Service, pk=svc_id)
    form = ServiceForm(instance=service)

    for field in form.fields.values():
        field.disabled = True

    context = {
        'h_form': form,
        'h_service': service
    }
    return render(request, 'mimascompany/create_service.html', context)
