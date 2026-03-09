from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from accounts.decorators import group_required


# Dentist dashboard
@login_required
@group_required(allowed_groups=['Dentists', 'Administrators', 'Employees'])
def dentist_dashboard(request):
    return render(request, 'dentists/dentist_dashboard.html')
