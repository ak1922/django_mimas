from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from accounts.decorators import group_required


# Patient dashboard
@login_required
@group_required(allowed_groups=['Administrators', 'Employees', 'Dentists'])
def patient_dashbaord(request):
    return render(request, 'patients/patient_dashboard.html')
