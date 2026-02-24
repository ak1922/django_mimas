from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from accounts.models import AccountUser
from accounts.decorators import group_required
from mimascompany.models.employee_model import Employee
from mimascompany.models.employeetasks_model import EmployeeTask, TaskCategory
from mimascompany.forms.employeetask_form import TaskCategoryForm, EmployeeTaskForm


# ------ Manage Task Categories ------
# Create employee task
@login_required
@group_required(allowed_groups=['Employees', 'Administrators'])
def create_task_category(request):

    if request.method == 'POST':
        form = TaskCategoryForm(request.POST)

        if form.is_valid():
            new_category = form.save()
            messages.success(request, f'New task category {new_category.name} created')
            return redirect('mimascompany:listtaskcategories')
    else:
        form = TaskCategoryForm()
    return render(request, 'mimascompany/create_taskcategory.html', {'h_form': form})


# List task categories
@login_required
@group_required(allowed_groups=['Employees', 'Administrators'])
def list_task_categories(request):

    all_categories = TaskCategory.objects.all()
    return render(request, 'mimascompany/list_taskcategory.html', {'h_allcategories': all_categories})


# Edit task category
@login_required
@group_required(allowed_groups=['Employees', 'Administrators'])
def edit_task_category(request, task_id):

    category = get_object_or_404(TaskCategory, pk=task_id)

    if request.method == 'POST':
        form = TaskCategoryForm(request.POST, instance=category)
        if form.is_valid():
            edited_category = form.save()
            messages.success(request, f'Category name {edited_category.name} updated.')
            return redirect('mimascompany:listtaskcategories')
        else:
            messages.error(request, 'Issues updating task category')
    else:
        form = TaskCategoryForm(instance=category)
    context = {
        'h_form': form,
        'h_taskcategory': category,
    }
    return render(request, 'mimascompany/create_taskcategory.html', context)


# Delete task category
@login_required
@group_required(allowed_groups=['Employees', 'Administrators'])
def delete_task_category(request, task_id):

    category = get_object_or_404(TaskCategory, pk=task_id)
    if request.method == 'POST':
        category.delete()
    return redirect('mimascompany:listtaskcategories')


# ------ Manage Employee Tasks ------
# Create task
@login_required
@group_required(allowed_groups=['Employees', 'Administrators'])
def create_task(request):

    if request.method == 'POST':
        form = EmployeeTaskForm(request.POST)
        if form.is_valid():
            new_task = form.save()
            messages.success(request, f'New task {new_task.task_name} created for {new_task.employee}.')
            return redirect('mimascompany:listtasks')
    else:
        form = EmployeeTaskForm()
    return render(request, 'mimascompany/create_employeetask.html', {'h_form': form})


# List tasks
@login_required
@group_required(allowed_groups=['Employees', 'Administrators'])
def list_tasks(request):

    all_tasks = EmployeeTask.objects.all()
    return render(request, 'mimascompany/list_employeetasks.html', {'h_alltasks': all_tasks})


# Edit task
@login_required
@group_required(allowed_groups=['Employees', 'Administrators'])
def edit_task(request, task_id):

    employee_task = get_object_or_404(EmployeeTask, pk=task_id)

    if request.method == 'POST':
        form = EmployeeTaskForm(request.POST, instance=employee_task)
        if form.is_valid():
            current_user = get_object_or_404(AccountUser, username=request.user)
            edited_task = form.save(commit=False)
            edited_task.updated_by = current_user
            edited_task.save()
            messages.success(request, f'Task {edited_task.task_name} for {edited_task.employee} updated.')
            return redirect('mimascompany:listtasks')
    else:
        form = EmployeeTaskForm(instance=employee_task)
    return render(request, 'mimascompany/create_employeetask.html', {'h_form': form})


# Delete task
@login_required
@group_required(allowed_groups=['Employees', 'Administrators'])
def delete_task(request, task_id):

    employee_task = get_object_or_404(EmployeeTask, pk=task_id)
    task_owner = get_object_or_404(Employee, user=employee_task.employee)

    if request.method == 'POST':
        employee_task.delete()
        messages.success(request, f'Task deleted for employee {task_owner}')
    return redirect('mimascompany:listtasks')
