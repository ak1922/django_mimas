from django import forms

from mimascompany.models.service_model import Service
from mimascompany.models.branch_model import Branch
from mimascompany.models.dentist_model import Dentist
from mimascompany.models.employee_model import Employee
from mimascompany.models.department_model import Department
from patients.models.patients_model import Patient
from patients.models.patientinsurance_model import PatientInsurance
from patients.models.patientappointment_model import PatientAppointment
from patients.models.patientvisit_models import PatientVisit, PostVisitOption, PatientVisitTask


# Patient visit form
class PatientVisitForm(forms.ModelForm):

    required_css_class = 'required'

    visit_title = forms.CharField(label='Visit Title')
    visit_status = forms.ChoiceField(
        label='Visit Status',
        choices=PatientVisit.VisitStatus.choices
    )
    visit_time = forms.CharField(label='Visit Time')
    visit_date = forms.DateField(
        label='Visit Date',
        widget=forms.DateInput(
            format='%Y=%m-%d', attrs={'type': 'date'}
        )
    )

    # ---- ForeignKeys ----
    patient = forms.ModelChoiceField(
        label='Patient',
        queryset=Patient.objects.all(),
        widget=forms.Select()
    )
    dentist = forms.ModelChoiceField(
        label='Dentist',
        queryset=Dentist.objects.all(),
        widget=forms.Select()
    )
    appointment = forms.ModelChoiceField(
        label='Appointment',
        required=False,
        queryset=PatientAppointment.objects.all(),
        widget=forms.Select
    )
    branch_name = forms.ModelChoiceField(
        label='Branch Name',
        queryset=Branch.objects.all(),
        widget=forms.Select()
    )
    insurance = forms.ModelChoiceField(
        label='Insurance',
        queryset=PatientInsurance.objects.all(),
        widget=forms.Select()
    )

    # ---- Many2Many ----
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
    visit_options = forms.ModelMultipleChoiceField(
        label='Visit Options',
        required=False,
        queryset=PostVisitOption.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ''
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'width: 400px'

    class Meta:
        model = PatientVisit
        fields = [
            'patient',
            'dentist',
            'branch_name',
            'appointment',
            'visit_title',
            'visit_date',
            'visit_time',
            'services',
            'departments',
            'visit_status',
            'visit_options'
        ]


# Employee task item
class PatientVisitTaskForm(forms.ModelForm):

    task_title = forms.CharField(label='Task Title')
    description = forms.CharField(
        label='Description',
        required=False,
        widget=forms.Textarea(
            attrs={'cols': 20, 'rows': 4}
        )
    )
    task_status = forms.ChoiceField(
        label='Task Status',
        choices=PatientVisitTask.STATUS_CHOICES,
        widget=forms.Select()
    )
    priority = forms.ChoiceField(
        label='Priority',
        choices=PatientVisitTask.Priority.choices,
        widget=forms.Select()
    )

    visit = forms.ModelChoiceField(
        label='Patient Visit',
        queryset=PatientVisit.objects.all(),
        widget=forms.Select()
    )
    assigned_to = forms.ModelChoiceField(
        label='Assigned To',
        queryset=Employee.active_employees.all(),
        widget=forms.Select()
    )

    class Meta:
        model = PatientVisitTask
        fields = [
            'assigned_to',
            'task_title',
            'visit',
            'task_status',
            'priority',
            'description',
        ]
