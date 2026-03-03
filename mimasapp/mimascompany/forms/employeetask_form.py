from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError

from mimascompany.models.employee_model import Employee
from mimascompany.models.employeetasks_model import EmployeeTask, TaskCategory


# Task form
class EmployeeTaskForm(forms.ModelForm):

    required_css_class = 'required'

    # ---- Task Info ----
    task_name = forms.CharField(label='Task Name')
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
    description = forms.CharField(
        label='Description',
        required=False,
        widget=forms.Textarea(
            attrs={'rows': 3, 'cols': 20}
        )
    )
    # ---- Related models ----
    employee = forms.ModelChoiceField(
        label='Employee',
        queryset=Employee.active_employees.all()
    )
    category = forms.ModelChoiceField(
        label='Task Category',
        required=True,
        empty_label='Choose Task Category.....',
        queryset=TaskCategory.objects.all()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ''
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'width: 400px'

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and timezone.is_naive(start_date):
            start_date = timezone.make_aware(start_date)
            cleaned_data['start_date'] = start_date

        if start_date and end_date and end_date < start_date:
            raise ValidationError(
                {'end_date': 'End date cannot be before start date.'}
            )

        if start_date and not self.instance.pk:
            if start_date < timezone.now():
                raise ValidationError("Start date cannot be in the past.")

        return self.cleaned_data

    class Meta:
        model = EmployeeTask
        exclude = ['updated_by']
        fields = [
            'employee',
            'task_name',
            'start_date',
            'end_date',
            'priority',
            'status',
            'category',
            'description'
        ]
