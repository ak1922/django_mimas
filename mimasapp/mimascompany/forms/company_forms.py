from django import forms

from mimascompany.models.service_model import Service
from mimascompany.models.department_model import Department
from mimascompany.models.branch_model import Branch
from mimascompany.models.employee_model import Employee
from mimascompany.models.bookings_model import PatientBooking


# Branch form
class BranchForm(forms.ModelForm):

    required_css_class = 'required'

    location = forms.CharField(max_length=50)
    branch_name = forms.CharField(label='Branch Name')

    branch_head = forms.ModelChoiceField(
        label='Branch Head',
        queryset=Employee.objects.all()
    )
    services = forms.ModelMultipleChoiceField(
        label='Services',
        queryset=Service.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )
    departments = forms.ModelMultipleChoiceField(
        label='Departments',
        queryset=Department.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Branch
        fields = '__all__'
        exclude = ['updated_by']

    def __init__(self, *args, **kwargs):
        super(BranchForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix= ''
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'width: 400px'




# Depratment form
class DepartmentForm(forms.ModelForm):

    required_css_class = 'required'

    department_name = forms.CharField(
        label='Department Name'
    )
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(
            attrs={'rows': 5, 'cols': 40}
        )
    )

    department_head = forms.ModelChoiceField(
        label='Department Head',
        queryset=Employee.objects.all()
    )

    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix= ''
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'width: 400px'

    class Meta:
        model = Department
        fields = '__all__'
        exclude = ['department_id', 'updated_by']


# Service form
class ServiceForm(forms.ModelForm):

    required_css_class = 'required'

    service_name = forms.CharField(label='Servive Name')
    price = forms.DecimalField(label='Price')
    duration = forms.IntegerField(label='Duration')
    description = forms.CharField(
        label='Description',
        required=False,
        widget=forms.Textarea(
            attrs={'rows': 5, 'cols': 40}
        )
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
    )

    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix= ''
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'width: 400px'

    class Meta:
        model = Service
        fields = '__all__'
        exclude = ['updated_by']


# Patient booking
class PatientBookingForm(forms.ModelForm):

    required_css_class = 'required'

    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    email = forms.EmailField(label='Email')

    message = forms.CharField(
        label='Message',
        widget=forms.Textarea(
            attrs={'rows': 5, 'cols': 40}
        )
    )

    def __init__(self, *args, **kwargs):
        super(PatientBookingForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix= ''
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'width: 400px'

    class Meta:
        model = PatientBooking
        fields = '__all__'
        exclude = ['updated_by']