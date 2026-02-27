from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from accounts.models import AccountUser
from accounts.decorators import group_required
from mimascompany.models.employee_model import Employee
from mimascompany.models.employeetasks_model import EmployeeTask, TaskCategory, EmployeeTaskItem
from mimascompany.forms.employeetask_form import TaskCategoryForm, EmployeeTaskForm, EmployeeTaskItemForm, \
    EmployeeTaskItemDashForm


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

    query = request.GET.get('item_name')
    all_categories = TaskCategory.objects.all().order_by('name')

    if query:
        all_categories = all_categories.filter(
            Q(name__icontains=query)
        ).distinct()
    else:
        all_categories = TaskCategory.objects.all().order_by('name')
    return render(request, 'mimascompany/list_taskcategory.html', {'h_allcategories': all_categories})


# Edit task category
@login_required
@group_required(allowed_groups=['Employees', 'Administrators'])
def edit_task_category(request, task_id):

    category = get_object_or_404(TaskCategory, pk=task_id)

    if request.method == 'POST':
        form = TaskCategoryForm(request.POST, instance=category)
        if form.is_valid():
            current_user = get_object_or_404(AccountUser, username=request.user)
            edited_category = form.save(commit=False)
            edited_category.updated_by = current_user
            edited_category.save()
            messages.success(request, f'Category name {edited_category.name} updated by {current_user}')
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

    query = request.GET.get('item_name')
    all_tasks = EmployeeTask.objects.all().order_by('start_date', 'priority')

    if query:
        all_tasks = all_tasks.filter(
            Q(task_name__icontains=query) |
            Q(status__icontains=query) |
            Q(priority__icontains=query) |
            Q(employee__last_name__icontains=query) |
            Q(employee__first_name__icontains=query) |
            Q(employee__user__username__icontains=query)
        ).distinct()
    else:
        all_tasks = EmployeeTask.objects.all().order_by('start_date', 'priority')

    paginator = Paginator(all_tasks, per_page=5)
    page_number = request.GET.get('page')
    page_alltasks = paginator.get_page(page_number)

    context = {
        'h_alltasks': all_tasks,
        'page_alltasks': page_alltasks
    }
    return render(request, 'mimascompany/list_employeetasks.html', context)


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
    task_items = EmployeeTaskItem.objects.filter(employee=task_owner).all()

    if request.method == 'POST':
        employee_task.delete()
        messages.success(request, f'Task deleted for employee {task_owner}')

    context = {
        'h_taskowner': task_owner,
        'h_taskitems': task_items,
        'h_employeetask': employee_task
    }
    return render(request, 'mimascompany/delete_employeetask.html', context)


# ---- Manage Task Items ----
# Create task item
@login_required
@group_required(allowed_groups=['Employees', 'Administrators'])
def create_task_item(request):

    if request.method == 'POST':
        form = EmployeeTaskItemForm(request.POST)
        if form.is_valid():
            new_item = form.save()
            messages.success(request, f'New task item {new_item.item_name} created for task {new_item.task_name}.')
            return redirect('mimascompany:listtaskitems')
        else:
            messages.error(request, 'Form submission error/s with task item.')
    else:
        form = EmployeeTaskItemForm()
    return render(request, 'mimascompany/create_taskitem.html', {'h_form': form})


# Create task item employee dash
@login_required
@group_required(allowed_groups=['Employees', 'Administrators'])
def create_item_employeedash(request, task_id=None):

    task_name = get_object_or_404(EmployeeTask, pk=task_id)
    employee = Employee.objects.filter(user=task_name.employee.user).first()

    if request.method == 'POST':
        form = EmployeeTaskItemDashForm(request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.task_name = task_name
            new_item.emlpoyee = employee
            new_item.save()
            messages.success(request, 'New item created')
            return redirect('mimascompany:employeedashboard')
        else:
            messages.error(request, 'Form submission error/s with task item.')
    else:
        form = EmployeeTaskItemDashForm(initial={
            'task_name': task_name,
            'employee': employee
        })

    return render(request, 'mimascompany/create_taskitem.html', {'h_form': form})


# Edit task item
@login_required
@group_required(allowed_groups=['Employees', 'Administrators'])
def edit_task_item(request, item_id):

    item = get_object_or_404(EmployeeTaskItem, pk=item_id)

    if request.method == 'POST':
        form = EmployeeTaskItemDashForm(request.POST, instance=item)
        if form.is_valid():
            current_user = get_object_or_404(AccountUser, username=request.user)
            edited_item = form.save(commit=False)
            edited_item.updated_by = current_user
            edited_item.save()
            messages.success(request, f'Task item {edited_item.item_name} for task {edited_item.task_name} updated.')
            return redirect('mimascompany:listtaskitems')
        else:
            messages.error(request, 'Form submission error/s with task item.')
    else:
        form = EmployeeTaskItemDashForm(instance=item)
    return render(request, 'mimascompany/create_taskitem.html', {'h_form': form})


# List task items
@login_required
@group_required(allowed_groups=['Employees', 'Administrators'])
def list_task_items(request):

    query = request.GET.get('item_name')
    all_taskitems = EmployeeTaskItem.objects.all().order_by('start_date')

    if query:
        all_taskitems = all_taskitems.filter(
            Q(item_name__icontains=query) |
            Q(employee__last_name__icontains=query) |
            Q(employee__first_name__icontains=query) |
            Q(task_name__task_name__icontains=query)
        ).distinct()
    else:
        all_taskitems = EmployeeTaskItem.objects.all().order_by('start_date')

    paginator = Paginator(all_taskitems, per_page=5)
    page_number = request.GET.get('page')
    page_alltaskitems = paginator.get_page(page_number)

    context = {
        'page_alltaskitems': page_alltaskitems,
        'h_allitemscount': all_taskitems.count()
    }
    return render(request, 'mimascompany/list_taskitems.html', context)


# Delete task item
@login_required
@group_required(allowed_groups=['Employees', 'Administrators'])
def delete_task_item(request, item_id):

    item = get_object_or_404(EmployeeTaskItem, pk=item_id)

    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Task item deleted.')
    return redirect('mimascompany:listtaskitems')
