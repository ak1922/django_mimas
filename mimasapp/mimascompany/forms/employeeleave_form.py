from django import forms

from mimascompany.models.leaverequests_model import LeaveRequest
from mimascompany.models.employee_model import Employee


# Leave form
class LeaveRequestForm(forms.ModelForm):

    start_date = forms.DateTimeField(
        label='Start Date',
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'}
        )
    )
    end_date = forms.DateTimeField(
        label='End Date',
        required=False,
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'}
        ),
    )
    leave_type = forms.ChoiceField(
        label='Leave Type',
        choices=LeaveRequest.LeaveType.choices,
        widget=forms.Select()
    )
    reason = forms.CharField(
        label='Reason',
        widget=forms.Textarea(attrs={'rows': 3, 'cols': 40})
    )

    # ---- Related models ----
    employee = forms.ModelChoiceField(
        label='Employee',
        empty_label='Choose Employee',
        widget=forms.Select(),
        queryset=Employee.active_employees.all()
    )

    class Meta:
        model = LeaveRequest
        fields = ['employee', 'start_date', 'end_date', 'leave_type', 'reason']
        exclude = ['updated_by']

    def __init__(self, *args, **kwargs):
        super(LeaveRequestForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label_suffix = ''
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'width: 400px'
