from django.urls import path

from .views.company import index, staff_room
from .views.manage_employee import EmployeeCreateView, list_employees, edit_employee, delete_employee, view_employee
from .views.manage_positions import edit_position, create_position, delete_position, list_positions
from .views.manage_employeetask import create_task_category, delete_task_category, edit_task_category, list_task_categories, \
    create_task, delete_task, edit_task, list_tasks, create_task_item, edit_task_item, list_task_items, delete_task_item, \
    create_item_employeedash
from .views.employee_dashboard import EmployeeDashboardView
from .views.manage_employeeleave import edit_leave_request, list_all_leaverequests, delete_leave_request, create_leave_request
from .views.manage_departments import create_department, edit_department, list_departments, delete_department, view_department
from .views.manage_branches import edit_branch, create_branch, list_branches, view_branch, delete_branch
from .views.manage_services import create_service, list_services, view_service, delete_service, edit_service
from .views.manage_employeedetails import create_employee_detail, create_employee_detail_employee, edit_employee_detail, \
    list_employee_details, delete_employee_detail
from .views.manage_employeecontact import create_employee_contact, edit_employee_contact, delete_employee_contact, \
    list_employee_contacts
from .views.manage_dentists import create_dentist, list_dentists, delete_dentist, edit_dentist, update_info_dentist_dash

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
    path('viewemployee/<int:emp_id>/view/', view_employee, name='viewemployee'),
    path('deleteemployee/<int:emp_id>/delete/', delete_employee, name='deleteemployee'),
    # Dentists
    path('listdentists/', list_dentists, name='listdentists'),
    path('createdentist/', create_dentist, name='createdentist'),
    path('editdentist/<int:den_id>/edit/', edit_dentist, name='editdentist'),
    path('deletedentist/<int:den_id>/delete/', delete_dentist, name='deletedentist'),
    path('updateinfodentistdash/<int:emp_id>/update/', update_info_dentist_dash, name='updateinfodentistdash'),
    # Branches
    path('listbranches/', list_branches, name='listbranches'),
    path('createbranch/', create_branch, name='createbranch'),
    path('editbranch/<int:bra_id>/edit/', edit_branch, name='editbranch'),
    path('viewbranch/<int:bra_id>/view/', view_branch, name='viewbranch'),
    path('deletebranch/<int:bra_id>/delete/', delete_branch, name='deletebranch'),
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
    # Employee Task items
    path('createtaskitem/', create_task_item, name='createtaskitem'),
    path('listtaskitems/', list_task_items, name='listtaskitems'),
    path('edittaskitem/<int:item_id>/edit/', edit_task_item, name='edittaskitem'),
    path('deletetaskitem/<int:item_id>/delete/', delete_task_item, name='deletetaskitem'),
    path('createitememployeedash/<int:task_id>/create/', create_item_employeedash, name='createitememployeedash'),
    # Services
    path('listservices/', list_services, name='listservices'),
    path('createservice/', create_service, name='createservice'),
    path('viewservice/<int:svc_id>/view/', view_service, name='viewservice'),
    path('editservice/<int:svc_id>/edit/', edit_service, name='editservice'),
    path('deleteservice/<int:svc_id>/delete/', delete_service, name='deleteservice'),
    # Departments
    path('createdepartment/', create_department, name='createdepartment'),
    path('listdepartments/', list_departments, name='listdepartments'),
    path('editdepartment/<int:dept_id>/edit/', edit_department, name='editdepartment'),
    path('viewdepartment/<int:dept_id>/view/', view_department, name='viewdepartment'),
    path('deletedepartment/<int:dept_id>/delete/', delete_department, name='deletedepartment'),
    # Employee Leave
    path('createleaverequest/', create_leave_request, name='createleaverequest'),
    path('listallleaverequests/', list_all_leaverequests, name='listallleaverequests'),
    path('editleaverequest/<int:req_id>/edit/', edit_leave_request, name='editleaverequest'),
    path('deleteleaverequest/<int:req_id>/delete/', delete_leave_request, name='deleteleaverequest'),
    # Employee Contact
    path('createemployeecontact/', create_employee_contact, name='createemployeecontact'),
    path('listemployeecontacts/', list_employee_contacts, name='listemployeecontacts'),
    path('editemployeecontact/<int:con_id>/edit/', edit_employee_contact, name='editemployeecontact'),
    path('deleteemployeecontact/<int:con_id>/delete/', delete_employee_contact, name='deleteemployeecontact'),
    # Employee Details
    path('listemployeedetails/', list_employee_details, name='listemployeedetails'),
    path('createemployeedetail/', create_employee_detail, name='createemployeedetail'),
    path('editemployeedetail/<int:det_id>/edit/', edit_employee_detail, name='editemployeedetail'),
    path('deleteemployeedetail/<int:det_id>/delete/', delete_employee_detail, name='deleteemployeedetail'),
    path('createemployeedetailemployee/<int:emp_id>/create/', create_employee_detail_employee, name='createemployeedetailemployee'),
]
