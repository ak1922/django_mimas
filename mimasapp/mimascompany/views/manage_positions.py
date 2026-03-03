import logging
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import AccountUser
from accounts.decorators import group_required
from mimascompany.models.employee_model import CompanyPositions
from mimascompany.forms.employee_form import CompanyPositionForm


# Set up logging
logger = logging.getLogger(__name__)

# Create position
@login_required
@group_required(allowed_groups=['Employees', 'Administrators'])
def create_position(request):

    if request.method == 'POST':
        form = CompanyPositionForm(request.POST)

        if form.is_valid():
            new_position = form.save()
            messages.success(request, f'New postion {new_position.title} created.')
            logger.info(f'Position {new_position.title} created by {request.user}.')
            return redirect('mimascompany:listpositions')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}:- {error}')
    else:
        form = CompanyPositionForm()

    context = {
        'h_form': form,
        'h_exists_position': None
    }
    return render(request, 'mimascompany/create_position.html', context)


# List positions
@login_required
@group_required(allowed_groups=['Employees', 'Administrators'])
def list_positions(request):

    query = request.GET.get('item_name')
    all_positions = CompanyPositions.objects.all().order_by('title')

    if query:
        all_positions = all_positions.filter(
            Q(title__icontains=query)
        ).distinct()
    else:
        all_positions = CompanyPositions.objects.all().order_by('title')

    paginator = Paginator(all_positions, per_page=5)
    page_number = request.GET.get('page')
    page_allpositions = paginator.get_page(page_number)

    context = {
        'page_allpositions': page_allpositions,
        'h_positionscount': all_positions.count()
    }
    return render(request, 'mimascompany/list_positions.html', context)


# Edit position
@login_required
@group_required(allowed_groups=['Employees', 'Administrators'])
def edit_position(request, pos_id):

    position = get_object_or_404(CompanyPositions, pk=pos_id)

    if request.method == 'POST':
        form = CompanyPositionForm(request.POST, instance=position)
        if form.is_valid():
            current_user = get_object_or_404(AccountUser, username=request.user)
            position_instance = form.save(commit=False)
            position_instance.updated_by = current_user
            position_instance.save()
            messages.success(request, f'Company position {position_instance.title} updated by {current_user}')
            logger.info(f'Company position {position_instance.title} updated by {current_user}')
            return redirect('mimascompany:listpositions')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}:- {error}')
    else:
        form = CompanyPositionForm(instance=position)
    return render(request, 'mimascompany/create_position.html', {'h_form': form})


# View position
@login_required
@group_required(allowed_groups=['Employees', 'Administrators'])
def view_position(request, pos_id):

    position = get_object_or_404(CompanyPositions, pk=pos_id)
    form = CompanyPositionForm(instance=position)

    for field in form.fields.values():
        field.disabled = True

    context = {
        'h_form': form,
        'h_exists_position': position
    }
    return render(request, 'mimascompany/create_position.html', context)


# Delete position
@login_required
@group_required(allowed_groups=['Employees', 'Administrators'])
def delete_position(request, pos_id):
    position = get_object_or_404(CompanyPositions, pk=pos_id)
    current_user = request.user
    if request.method == 'POST':
        logger.info(f'{current_user} requesting delete of company position {position.title}. Proceeding to delete.')
        position.delete()
        messages.success(request, 'Position deleted.')
        logger.info('Position deleted.')
    return redirect('mimascompany:listpositions')
