import logging
from django.contrib import messages
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
            logger.info(f'Position {new_position.title} create.')
            return redirect('mimascompany:listpositions')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}:- {error}')
    else:
        form = CompanyPositionForm()
    return render(request, 'mimascompany/create_position.html', {'h_form': form})


# List positions
@login_required
@group_required(allowed_groups=['Employees', 'Administrators'])
def list_positions(request):

    all_positions = CompanyPositions.objects.all()
    context = {
        'h_allpositions': all_positions,
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
