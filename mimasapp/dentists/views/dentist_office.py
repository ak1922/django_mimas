from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from accounts.decorators import group_required


# Dentist office
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators', 'Employees'])
def dentist_office(request):
    return render(request, 'dentists/dentist_office.html')
