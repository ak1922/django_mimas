from django.shortcuts import render

from mimascompany.models.employee_model import Employee
from mimascompany.models.dentist_model import Dentist
from mimascompany.models.department_model import Department
from mimascompany.models.service_model import Service
from mimascompany.models.branch_model import Branch
from patients.models import PatientBill

# Main index page
def index(request):
    return render(request, 'index.html')


# Staff room
def staff_room(request):

    allbills = PatientBill.objects.all().count()
    all_employees = Employee.objects.all().count()
    all_dentists = Dentist.objects.all().count()
    all_services = Service.objects.all().count()
    all_branches = Branch.objects.all().count()
    all_departments = Department.objects.all().count()

    context = {
        'h_allbills': allbills,
        'h_allemployees': all_employees,
        'h_alldentists': all_dentists,
        'h_allservices': all_services,
        'h_allbranches': all_branches,
        'h_alldepartments': all_departments
    }
    return render(request, 'mimascompany/staffroom.html', context)
