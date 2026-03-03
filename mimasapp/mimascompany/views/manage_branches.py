from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from accounts.models import AccountUser
from accounts.decorators import group_required
from mimascompany.models.branch_model import Branch
from mimascompany.forms.company_forms import BranchForm
from mimascompany.models.department_model import Department


# Create branch
@login_required
@group_required(allowed_groups=['Dentists', 'Employees', 'Administrators'])
def create_branch(request):

    if request.method == 'POST':
        form = BranchForm(request.POST)

        if form.is_valid():
            new_branch = form.save(commit=False)
            new_branch.save()
            form.save_m2m()
            messages.success(request, f'New branch {new_branch.branch_name} created.')
            return redirect('mimascompany:listbranches')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.title()}:- {error}')
    else:
        form = BranchForm()

    departments = Department.objects.prefetch_related('service_department').all()
    context = {
        'h_form': form,
        'h_departments': departments,
        'h_exists_branch': None
    }
    return render(request, 'mimascompany/create_branch.html', context)


# List branches
@login_required
@group_required(allowed_groups=['Dentists', 'Employees', 'Administrators'])
def list_branches(request):

    query = request.GET.get('item_name')
    all_branches = Branch.objects.all().order_by('created')

    if query:
        all_branches = all_branches.filter(
            Q(branch_name__icontains=query) |
            Q(branch_head__last_name__icontains=query) |
            Q(branch_head__first_name__icontains=query) |
            Q(departments__department_name__icontains=query)
        ).distinct()
    else:
        all_branches = Branch.objects.all().order_by('created')

    paginator = Paginator(all_branches, per_page=5)
    page_number = request.GET.get('page')
    page_allbranches = paginator.get_page(page_number)

    context = {
        'page_allbranches': page_allbranches,
        'h_allbranchescount': all_branches.count()
    }
    return render(request, 'mimascompany/list_branches.html', context)


# Edit branch
@login_required
@group_required(allowed_groups=['Dentists', 'Employees', 'Administrators'])
def edit_branch(request, bra_id):

    branch = Branch.objects.get(pk=bra_id)

    if request.method == 'POST':
        form = BranchForm(request.POST, instance=branch)

        if form.is_valid():
            current_user = AccountUser.objects.get(username=request.user)
            edited_branch = form.save(commit=False)
            edited_branch.modified_by = current_user
            edited_branch.save()
            form.save_m2m()
            messages.success(request, f'Information for branch {edited_branch.branch_name}, updated.')
            return redirect('mimascompany:listbranches')
        else:
            messages.error(request, 'Issues with branch information update.')

    else:
        form = BranchForm(instance=branch)

    selected_service_ids = branch.services.values_list('id', flat=True)
    selected_dept_ids = branch.departments.values_list('department_id', flat=True)
    departments = Department.objects.prefetch_related('service_department').all()

    context = {
        'h_form': form,
        'h_departments': departments,
        'h_selecteddeptids': selected_dept_ids,
        'h_selectedserviceids': selected_service_ids
    }
    return render(request, 'mimascompany/create_branch.html', context)


# Delete branch
@login_required
@group_required(allowed_groups=['Dentists', 'Employees', 'Administrators'])
def delete_branch(request, bra_id):

    branch = Branch.objects.get(pk=bra_id)
    if request.method == 'POST':
        branch.delete()
        messages.success(request, 'Branch deleted.')
    return redirect('mimascompany:listbranches')


# View Branch
@login_required
@group_required(allowed_groups=['Dentists', 'Employees', 'Administrators'])
def view_branch(request, bra_id):
    """ Read only view """

    branch = Branch.objects.get(pk=bra_id)
    form = BranchForm(instance=branch)

    for field in form.fields.values():
        field.disabled = True

    selected_service_ids = branch.services.values_list('id', flat=True)
    selected_dept_ids = branch.departments.values_list('department_id', flat=True)
    departments = Department.objects.prefetch_related('service_department').all()

    context = {
        'h_form': form,
        'h_branch': branch,
        'h_exists_branch': branch,
        'h_departments': departments,
        'h_selecteddeptids': selected_dept_ids,
        'h_selectedserviceids': selected_service_ids
    }
    return render(request, 'mimascompany/create_branch.html', context)
