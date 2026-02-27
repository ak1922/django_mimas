from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from mimascompany.models.employeetasks_model import TaskCategory, EmployeeTask, EmployeeTaskItem

# Task category form
class TaskCategoryForm(forms.ModelForm):

    class Meta:
        model = TaskCategory
        fields = '__all__'
        exclude = ['updated_by']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 400px'}),
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 45, 'class': 'form-control'}),
        }


# Task form
class EmployeeTaskForm(forms.ModelForm):

    class Meta:
        model = EmployeeTask
        fields = ['task_name', 'description', 'start_date', 'end_date', 'priority', 'status', 'category', 'employee']
        exclude = ['updated_by']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 20}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            self.fields[field].widget.attrs.update({'style': 'width: 400px'})

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise ValidationError(
                {'end_date': 'End date cannot be before start date.'}
            )

        # Ensure start date is not in the past for new tasks
        if not self.instance.pk and start_date and start_date < timezone.now():
            raise ValidationError(
                {'start_date': 'Start date cannot be in the past.'}
            )
        return cleaned_data


# Task item form
class EmployeeTaskItemForm(forms.ModelForm):

    class Meta:
        model = EmployeeTaskItem
        fields = ['item_name', 'task_name', 'employee', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            self.fields[field].widget.attrs.update({'style': 'width: 400px'})



class EmployeeTaskItemDashForm(forms.ModelForm):

    class Meta:
        model = EmployeeTaskItem
        fields = ['item_name', 'task_name', 'employee', 'start_date', 'end_date', 'comments']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'comments': forms.Textarea(attrs={'rows': 3, 'cols': 20}),
        }

    def __init__(self, *args, **kwargs):
        super(EmployeeTaskItemDashForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ''
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'width: 400px'
