from django import forms

from mimascompany.models.employee_model import Employee
from mimascompany.models.department_model import Department
from mimascompany.models.employeedetails_model import EmployeeDetail


# Employee detail form
class EmployeeDetailForm(forms.ModelForm):

    required_css_class = 'required'

    # ---- Employee personal info ----
    ssn = forms.CharField(label='SSN')
    address = forms.CharField(label='Address')
    phone_number = forms.CharField(label='Phone Number')
    date_hired = forms.DateField(
        label='Date Hired',
        widget= forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})
    )

    # ---- Spouse section ----
    spouse_name = forms.CharField(
        required=False,
        label='Spouse Name'
    )
    spouse_address = forms.CharField(
        label='Spouse Address',
        required=False
    )
    spouse_employer = forms.CharField(
        required=False,
        label='Spouse Employer'
    )
    spouse_employer_address = forms.CharField(
        required=False,
        label='Spouse Employer Address'
    )
    marital_status = forms.ChoiceField(
        choices=EmployeeDetail.MaritalStatus.choices,
        widget=forms.Select
    )

    # ---- ForeignKeys ----
    employee = forms.ModelChoiceField(
        label='Employee',
        empty_label='Choose Employee',
        queryset=Employee.objects.all()
    )
    supervisor = forms.ModelChoiceField(
        label='Supervisor',
        empty_label='Choose Supervisor',
        queryset=Employee.objects.all()
    )
    department = forms.ModelChoiceField(
        label='Department',
        empty_label='Choose Department',
        queryset=Department.objects.all()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ''
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'width: 400px'

        # Check foe employees with details when creating and editing
        existing_details = EmployeeDetail.objects.values_list('employee_id', flat=True)
        without_details = Employee.objects.exclude(user_id__in=existing_details)

        if self.instance and self.instance.pk:
            self.fields['employee'].queryset = without_details | Employee.objects.filter(pk=self.instance.employee_id)
        else:
            self.fields['employee'].queryset = without_details
            self.fields['employee'].empty_label = 'Select an Employee....'

    class Meta:
        model = EmployeeDetail
        fields = [
            'employee',
            'ssn',
            'supervisor',
            'department',
            'date_hired',
            'address',
            'phone_number',
            'marital_status',
            'spouse_name',
            'spouse_address',
            'spouse_employer',
            'spouse_employer_address'
        ]
        exclude = ['updated_by']
