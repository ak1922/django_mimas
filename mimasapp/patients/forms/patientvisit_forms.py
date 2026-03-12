from django import forms

from mimascompany.models.service_model import Service
from mimascompany.models.branch_model import Branch
from mimascompany.models.dentist_model import Dentist
from mimascompany.models.department_model import Department
from patients.models.patients_model import Patient
from patients.models.patientinsurance_model import PatientInsurance
from patients.models.patientappointment_model import PatientAppointment
from patients.models.patientvisit_models import PatientVisit, PostVisitOption
from patients.models.treatmentroom_model import TreatmentRoom


# Patient visit form
class PatientVisitForm(forms.ModelForm):

    required_css_class = 'required'

    visit_title = forms.CharField(label='Visit Title')
    visit_status = forms.ChoiceField(
        label='Visit Status',
        choices=PatientVisit.VISIT_STATUS
    )

    visit_time = forms.ChoiceField(
        label='Visit Time',
        choices=PatientVisit.VISIT_TIME
    )
    visit_date = forms.DateField(
        label='Visit Date',
        widget=forms.DateInput(
            format='%Y-%m-%d', attrs={'type': 'date'}
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
    branch = forms.ModelChoiceField(
        label='Branch',
        queryset=Branch.objects.all(),
        widget=forms.Select()
    )
    insurance = forms.ModelChoiceField(
        label='Insurance',
        required=False,
        queryset=PatientInsurance.objects.all(),
        widget=forms.Select()
    )
    treatment_room = forms.ModelChoiceField(
        label='Treatment Room',
        queryset=TreatmentRoom.cust_treatments.is_available().all(),
        widget=forms.Select(),
        required=False,
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

        for field_name, field in self.fields.items():
            field.label_suffix = ''

            if not isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['style'] = 'width: 400px'

    class Meta:
        model = PatientVisit
        fields = [
            'patient',
            'dentist',
            'branch',
            'appointment',
            'visit_title',
            'visit_date',
            'visit_time',
            'services',
            'departments',
            'visit_status',
            'visit_options',
            'treatment_room'
        ]
