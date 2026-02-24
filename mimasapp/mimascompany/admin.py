from django.contrib import admin

from .models.employee_model import CompanyPositions, Employee
from .models.employeetasks_model import TaskCategory, EmployeeTask
from .models.leaverequests_model import LeaveRequest


@admin.register(CompanyPositions)
class CompanyPositionsAdmin(admin.ModelAdmin):

    list_display = ['title', 'description', 'created', 'updated', 'updated_by']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    list_display = ['first_name', 'last_name', 'gender', 'status', 'vacations_days_accrued', 'vacation_days_remaining']


@admin.register(EmployeeTask)
class EmployeeTaskAdmin(admin.ModelAdmin):

    list_display = ['task_name', 'description', 'start_date', 'end_date', 'priority', 'status']


@admin.register(TaskCategory)
class TaskCategoryAdmin(admin.ModelAdmin):

    list_display = ['name', 'description']


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'end_date', 'requested_date', 'leave_type', 'days_taken']
