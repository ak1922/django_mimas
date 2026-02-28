from django.contrib import admin

from .models.employee_model import CompanyPositions, Employee
from .models.employeetasks_model import TaskCategory, EmployeeTask, EmployeeTaskItem
from .models.leaverequests_model import LeaveRequest
from .models.bookings_model import PatientBooking
from .models.branch_model import Branch
from .models.service_model import Service
from .models.department_model import Department
from .models.dentist_model import Dentist
from .models.employeedetails_model import EmployeeDetail
from .models.employeecontact_model import EmployeeContact


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['branch_name', 'branch_head', 'location']
    search_fields = ['services__service_name', 'departments__department_name', 'branch_name', 'branch_head__last_name', 'branch_head__first_name']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['service_name', 'description', 'department', 'created', 'updated', 'updated_by']
    search_fields = ['service_name']
    
   
@admin.register(Dentist)
class DentistAdmin(admin.ModelAdmin):
       list_display = ['employee', 'branch_name', 'supervisor', 'specialty', 'created', 'updated', 'updated_by']
       search_fields = ['employee__last_name', 'employee__first_name']
       
       
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['department_name', 'department_head', 'description', 'created', 'updated', 'updated_by']
    search_fields = ['department_name', 'department_head__last_name', 'department_head__first_name']


@admin.register(EmployeeDetail)
class EmployeeDetailAdmin(admin.ModelAdmin):
    list_display = ['employee', 'ssn', 'address', 'phone_number', 'date_hired', 'created', 'updated', 'updated_by']
    search_fields = ['employee__last_name', 'employee__first_name', 'supervisor__last_name', 'supervisor__first_name']


@admin.register(EmployeeContact)
class EmployeeEMContactAdmin(admin.ModelAdmin):
    list_display = ['employee', 'contact_name', 'contact_phone', 'created', 'updated', 'updated_by']
    search_fields = ['employee__last_name', 'employee__first_name', 'contact_name']


@admin.register(CompanyPositions)
class CompanyPositionsAdmin(admin.ModelAdmin):

    list_display = ['title', 'description', 'created', 'updated', 'updated_by']
    search_fields = ['title']
    list_per_page = 6


@admin.register(PatientBooking)
class PatientBookingAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'created', 'updated', 'updated_by']
    search_fields = ['first_name', 'last_name', 'email']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    list_display = ['first_name', 'last_name', 'gender', 'status', 'vacations_days_accrued', 'vacation_days_remaining']
    search_fields = ['status', 'first_name', 'last_name']
    list_per_page = 10


@admin.register(EmployeeTask)
class EmployeeTaskAdmin(admin.ModelAdmin):

    list_display = ['task_name', 'description', 'start_date', 'end_date', 'priority', 'status']
    search_fields = ['status', 'employee__user__username', 'priority', 'task_name']
    list_per_page = 10

@admin.register(TaskCategory)
class TaskCategoryAdmin(admin.ModelAdmin):

    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'end_date', 'requested_date', 'leave_type', 'days_taken']
    search_fields = ['employee__user__username', 'approved_by__employee_accountuser__first_name', 'approved_by__employee_accountuser__last_name',
                     'employee__first_name', 'employee__last_name']


@admin.register(EmployeeTaskItem)
class EmployeeTaskItemAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'employee', 'task_name', 'start_date', 'end_date']
    list_per_page = 10
    search_fields = ['item_name', 'employee__last_name', 'employee__first_name', 'task_name__task_name']
    ordering = ['end_date']
    