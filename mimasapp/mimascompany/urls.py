from django.urls import path

from .views.company import index, staff_room
from .views.manage_employee import EmployeeCreateView, list_employees, edit_employee, delete_employee
from .views.manage_positions import edit_position, create_position, delete_position, list_positions
from .views.manage_employeetask import create_task_category, delete_task_category, edit_task_category, list_task_categories, \
    create_task, delete_task, edit_task, list_tasks
from .views.employee_dashboard import EmployeeDashboardView
from .views.manage_employeeleave import edit_leave_request, list_all_leaverequests, delete_leave_request, create_leave_request

app_name = 'mimascompany'

urlpatterns = [
    path('', index, name='index'),
    path('staffroom/', staff_room, name='staffroom'),
    # Employee Dashboard
    path('employeedashboard/', EmployeeDashboardView.as_view(), name='employeedashboard'),
    # Employees
    path('listemployees/', list_employees, name='listemployees'),
    path('createemployee/', EmployeeCreateView.as_view(), name='createemployee'),
    path('editemployee/<int:emp_id>/edit/', edit_employee, name='editemployee'),
    path('deleteemployee/<int:emp_id>/delete/', delete_employee, name='deleteemployee'),
    # Positions
    path('listpositions/', list_positions, name='listpositions'),
    path('createposition/', create_position, name='createposition'),
    path('editposition/<int:pos_id>/edit/', edit_position, name='editposition'),
    path('deleteposition/<int:pos_id>/delete/', delete_position, name='deleteposition'),
    # Task Categories
    path('createtaskcategory/', create_task_category, name='createtaskcategory'),
    path('listtaskcategories/', list_task_categories, name='listtaskcategories'),
    path('edittaskcategory/<int:task_id>/edit/', edit_task_category, name='edittaskcategory'),
    path('deletetaskcategory/<int:task_id>/delete/', delete_task_category, name='deletetaskcategory'),
    # Employee Tasks
    path('listtasks/', list_tasks, name='listtasks'),
    path('createtask/', create_task, name='createtask'),
    path('edittask/<int:task_id>/edit/', edit_task, name='edittask'),
    path('deletetask/<int:task_id>/delete/', delete_task, name='deletetask'),
    # Services
    # Departments
    # Employee Leave
    path('createleaverequest/', create_leave_request, name='createleaverequest'),
    path('listallleaverequests/', list_all_leaverequests, name='listallleaverequests'),
    path('editleaverequest/<int:req_id>/edit/', edit_leave_request, name='editleaverequest'),
    path('deleteleaverequest/<int:req_id>/delete/', delete_leave_request, name='deleteleaverequest'),
    # Employee Contact
    # Employee Details
]
