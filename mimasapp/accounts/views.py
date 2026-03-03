import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404

from .models import AccountUser
from .forms import RegisterAppUserForm, AppLoginForm


# Logging setup
logger = logging.getLogger(__name__)


# Register user
def register_user(request):

    if request.method == 'POST':
        form = RegisterAppUserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.save()
            logger.info(f'New user created for {new_user}')
            return redirect('mimascompany:index')
        else:
            for field, errors in form.errors.items():
                messages.error(request, f'{field}:- {", ".join(errors)}')
    else:
        form = RegisterAppUserForm()
    return render(request, 'accounts/register.html', {'h_form': form})


# Login view
def account_login(request):

    if request.method == 'POST':
        form = AppLoginForm(request.POST)
        if form.is_valid():
            user_data = form.cleaned_data
            user = authenticate(request, username=user_data['email'], password=user_data['password'])
            if user is not None:
                login(request, user)
                logger.info(f'User {user} logged in.')
                return redirect('mimascompany:index')
            else:
                messages.error(request, 'Invalid email or password provided.')
        else:
            for field, errors in form.errors.items():
                messages.error(request, f'{field}:- {", ".join(errors)}')
    else:
        form = AppLoginForm()
    return render(request, 'accounts/login.html', {'h_form': form})


# Logout user
@login_required
def account_logout(request, usr_id):

    loggedin_user = get_object_or_404(AccountUser, pk=usr_id)
    logout(request)
    logger.info(f'User {loggedin_user} logged in.')
    return redirect('mimascompany:index')
