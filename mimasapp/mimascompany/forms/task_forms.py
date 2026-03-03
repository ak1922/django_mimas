from django import forms

from mimascompany.models.employee_model import Employee
from mimascompany.models.employeetasks_model import TaskCategory, EmployeeTask, EmployeeTaskItem


# Task category form
class TaskCategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ''

    class Meta:
        model = TaskCategory
        fields = '__all__'
        exclude = ['updated_by']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 400px'}),
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 45, 'class': 'form-control'}),
        }


# Task item form
class EmployeeTaskItemForm(forms.ModelForm):

    required_css_class = 'required'

    # ---- Item info ----
    item_name = forms.CharField(label='Item Name')

    # ---- Related models ----
    employee = forms.ModelChoiceField(
        label='Employee',
        queryset=Employee.active_employees.all()
    )
    task_name = forms.ModelChoiceField(
        label='Task Name',
        queryset=EmployeeTask.objects.all()
    )
    start_date = forms.DateTimeField(
        label='Start Date',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    end_date = forms.DateTimeField(
        label='End Date',
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ''
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'width: 400px'

    class Meta:
        model = EmployeeTaskItem
        fields = [
            'employee',
            'task_name',
            'item_name',
            'start_date',
            'end_date'
        ]


# Task item form for employee dashboard
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
