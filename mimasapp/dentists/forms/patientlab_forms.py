from django import forms

from mimascompany.models.branch_model import Branch
from mimascompany.models.dentist_model import Dentist
from patients.models.patients_model import Patient
from patients.models.patientvisit_models import PatientVisit
from patients.models.patientinsurance_model import PatientInsurance
from patients.models.patientappointment_model import PatientAppointment
from patients.models.patientlab_model import PatientLab


class PatientLabForm(forms.ModelForm):

    required_css_class = 'required'

    lab_title = forms.CharField(label='Lab Title')
    lab_name = forms.CharField(
        label='Laboratory Name',
        required=False
    )
    lab_address = forms.CharField(
        label='Laboratory Address',
        required=False
    )
    lab_phone = forms.CharField(
        label='Laboratory Phone',
        required=False
    )
    due_date = forms.DateField(
        label='Due Date',
        widget=forms.DateInput(
            format='%Y-%m-%d', attrs={'type': 'date'}
        )
    )
    instructions = forms.CharField(
        required=False,
        label='Instructions',
        widget=forms.Textarea(
            attrs={'rows': 3, 'cols': 20}
        )
    )
    closed = forms.BooleanField(
        label='Closed',
        required=False,
        widget=forms.CheckboxInput()
    )

    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        label='Patient',
        widget=forms.Select()
    )
    dentist = forms.ModelChoiceField(
        label='Dentist',
        widget=forms.Select(),
        queryset=Dentist.objects.all()
    )
    branch = forms.ModelChoiceField(
        label='Branch',
        queryset=Branch.objects.all(),
        widget=forms.Select()
    )
    insurance = forms.ModelChoiceField(
        label='Insurance',
        queryset=PatientInsurance.objects.all(),
        required=False,
        widget=forms.Select()
    )
    appointment = forms.ModelChoiceField(
        label='Patient Appointment',
        required=False,
        queryset=PatientAppointment.objects.all(),
        widget=forms.Select()
    )
    visit = forms.ModelChoiceField(
        label='Patient Visit',
        queryset=PatientVisit.objects.all(),
        widget=forms.Select()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.label_suffix = ''

            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['style'] = 'width: 400px'

    class Meta:
        model = PatientLab
        exclude = ['updated_by']
        fields = [
            'patient',
            'dentist',
            'branch',
            'visit',
            'lab_title',
            'due_date',
            'appointment',
            'insurance',
            'lab_name',
            'lab_phone',
            'lab_address',
            'closed',
            'instructions'
        ]
