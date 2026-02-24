from django.utils import timezone
from django.db.models import Q
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from mimascompany.models.employeetasks_model import EmployeeTask
from mimascompany.models.leaverequests_model import LeaveRequest

# Employee dashboard
class EmployeeDashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):

    model = EmployeeTask
    template_name = 'mimascompany/employee_dashboard.html'
    context_object_name = 'tasks'

    def test_func(self):
        """Restrict access to Administrators or Employees."""
        allowed_groups = ['Administrators', 'Employees']
        return self.request.user.groups.filter(name__in=allowed_groups).exists()

    def get_queryset(self):
        return EmployeeTask.objects.filter(employee=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = self.get_queryset()

        userleave_requests = LeaveRequest.objects.filter(employee=self.request.user.id).order_by('start_date')
        context['leave_requests'] = userleave_requests

        context['leave_stats'] = {
            'total': userleave_requests.count(),
            'pending': userleave_requests.filter(status=LeaveRequest.ApprovalStatus.PENDING).count(),
            'approved': userleave_requests.filter(status=LeaveRequest.ApprovalStatus.APPROVED).count(),
        }

        context['stats'] = {
            'h_total': tasks.count(),
            'h_todo': tasks.filter(status=EmployeeTask.Status.TODO).count(),
            'in_progress': tasks.filter(status=EmployeeTask.Status.IN_PROGRESS).count(),
            'completed': tasks.filter(status=EmployeeTask.Status.COMPLETED).count(),
            'overdue': tasks.filter(
                ~Q(status=EmployeeTask.Status.COMPLETED),
                end_date__lt=timezone.now()
            ).count(),
        }

        context['high_priority'] = tasks.filter(priority=4).count()
        context['h_employee'] = tasks.filter(employee=self.request.user.id)
        return context
