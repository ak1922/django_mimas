import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from accounts.decorators import group_required
from patients.models.treatmentroom_model import TreatmentRoom
from patients.forms.treatmentroom_form import TreatmentRoomForm
from patients.forms.archived_readonly_forms import TreatmentRoomReadOnlyForm
from mimascompany.models.employee_model import Employee


logger = logging.getLogger(__name__)


# Create treatment room
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def create_treatment_room(request):

    if request.method == 'POST':
        form = TreatmentRoomForm(request.POST)

        if form.is_valid():
            new_room = form.save()
            messages.success(request, f'New treatment room {new_room.room_name} created by {request.user}.')
            logger.info(f'New treatment room {new_room.room_name} created by {request.user}.')
            return redirect('patients:listtreatmentrooms')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field} - {error}')
                    logger.error(f'Treatment Room Form:-{field} - {error}')
    else:
        form = TreatmentRoomForm()

    context = {
        'h_form': form,
        'h_exists_room': None
    }
    return render(request, 'patients/create_treatmentroom.html', context)


# Edit treatment room
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def edit_treatment_room(request, room_id):

    room = get_object_or_404(TreatmentRoom, pk=room_id)
    if request.method == 'POST':
        form = TreatmentRoomForm(request.POST, instance=room)
        if form.is_valid():
            current_user = get_object_or_404(Employee, user=request.user)
            edited_room = form.save(commit = False)
            edited_room.updated_by = current_user
            edited_room.save()
            messages.success(request, f'Treatment room {edited_room.room_name} updated.')
            logger.info(f'Treatment room {edited_room.room_name} updated by {request.user}')
            return redirect('patients:listtreatmentrooms')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field} - {error}')
                    logger.error(f'Treatment Room Form:-{field} - {error}')
    else:
        form = TreatmentRoomForm(instance=room)
    return render(request, 'patients/create_treatmentroom.html', {'h_form': form})


# View treatment room
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def view_treatment_room(request, room_id):

    room = get_object_or_404(TreatmentRoom, pk=room_id)
    form = TreatmentRoomReadOnlyForm(instance=room)

    context = {
        'h_form': form,
        'h_exists_room': room
    }
    return render(request, 'patients/create_treatmentroom.html', context)



# List treatment rooms
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def list_treatment_rooms(request):

    all_rooms = TreatmentRoom.objects.all()
    context = {
        'h_allrooms': all_rooms,
        'h_allroomstotal': all_rooms.count()
    }
    return render(request, 'patients/list_treatmentrooms.html', context)


# Delete treatment room
@login_required
@group_required(allowed_groups=['Administrators', 'Dentists', 'Employees'])
def delete_treatment_room(request, room_id):

    room = get_object_or_404(TreatmentRoom, pk=room_id)
    if request.method == 'POST':
        room.delete()
        messages.success(request, f'Treatment room deleted')
        logger.info(f'Treatment room deleted by {request.user}')
    return redirect('patients:listtreatmentrooms')
