import logging
from django.db import transaction
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from mimascompany.models import PatientBooking
from mimascompany.forms import PatientBookingForm
from mimascompany.utils import generate_username
from patients.models import PatientMessage
from patients.forms import PatientForm
from accounts.models import AccountUser
from accounts.decorators import group_required


logger = logging.getLogger(__name__)


# Create booking
def create_customer_booking(request):

    if request.method == 'POST':
        form = PatientBookingForm(request.POST)

        if form.is_valid():
            # Create new booking
            new_booking = form.save(commit=False)

            firstname = new_booking.first_name
            lastname = new_booking.last_name
            customer_username = generate_username(firstname, lastname)
            new_booking.username = customer_username
            form.save()

            messages.success(request, 'Thanks for booking an appointment, we\'ll be in touch with you shortly.')
            booking_message = f'New customer booking created for {new_booking.first_name} {new_booking.last_name}'
            PatientMessage.objects.create(
                is_active=True,
                message=booking_message
            )

            # Create new app user
            new_app_user = AccountUser.objects.create_user(
                username=customer_username,
                password='GoodPassword',
                user_type='Patients',
                email=new_booking.email
            )
            messages.success(request, f'Your username is {new_app_user.username}')
            logger.info(f'Your username is {new_app_user.username}')
            return redirect('mimascompany:index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field} - {error}')
    else:
        form = PatientBookingForm()

    context = {
        'h_form': form,
        'h_existing_booking': None
    }
    return render(request, 'mimascompany/create_booking.html', context)


# List bookings
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def list_customers_bookookings(request):

    allbookings = PatientBooking.objects.all()

    context = {
        'h_allbooking': allbookings,
        'h_bookingstotal': allbookings.count()
    }
    return render(request, 'mimascompany/list_bookings.html', context)


# View booking
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def view_customer_booking(request, book_id):

    booking = get_object_or_404(PatientBooking, pk=book_id)
    form = PatientBookingForm(instance=booking)

    for field in form.fields.values():
        field.disabled = True

    context = {
        'h_form': form,
        'h_existing_booking': booking
    }
    return render(request, 'mimascompany/create_booking.html', context)


# Delete booking
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def delete_customer_booking(request, book_id):

    booking = get_object_or_404(PatientBooking, pk=book_id)
    if request.method == 'POST':
        logger.info(f'Booking {booking} request by {request.user}.')
        booking.delete()
        messages.success(request, 'Customer booking deleted.')
        logger.info('Customer booking deleted.')
    return redirect('mimascompany:listcustomersbookookings')


# Create patient from booking
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def create_patient_with_booking(request, book_id):

    booking = get_object_or_404(PatientBooking, pk=book_id)
    account_user = get_object_or_404(AccountUser, email=booking.email)

    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():

            try:
                with transaction.atomic():
                    new_patient = form.save(commit=False)
                    new_patient.patient = account_user
                    new_patient.first_name = booking.first_name
                    new_patient.last_name = booking.last_name
                    form.save()
                    booking.delete()
                    messages.success(request, f'New patient created for {booking.username}')
                    logger.info(f'New patient created for {booking.username}, booking deleted.')
                return redirect('mimascompany:listcustomersbookookings')
            except Exception as e:
                messages.error(request, f'Error: {e}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field} - {error}')
    else:
        form = PatientForm(initial={
            'patient': account_user,
            'first_name': booking.first_name,
            'last_name': booking.last_name
        })
    return render(request, 'patients/create_patient.html', {'h_form': form})
