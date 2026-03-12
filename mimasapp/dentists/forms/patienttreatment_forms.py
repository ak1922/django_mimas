from django import forms

from mimascompany.models.branch_model import Branch
from mimascompany.models.dentist_model import Dentist
from patients.models.patients_model import Patient
from patients.models.patientvisit_models import PatientVisit
from patients.models.patienttreatment_model import PatientTreatment
from patients.models.patientinsurance_model import PatientInsurance
from patients.models.patientappointment_model import PatientAppointment


# Treatment form
class PatientTreatmentForm(forms.ModelForm):

    required_css_class = 'required'

    treatment_title = forms.CharField(label='Treatment Title')
    teeth_number = forms.CharField(
        required=False,
        label='Teeth Number'
    )
    medication = forms.CharField(
        label='Medication',
        required=False
    )
    notes = forms.CharField(
        required=False,
        label='Notes',
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
        label='Patients',
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
        model = PatientTreatment
        exclude = ['updated_by']
        fields = [
            'patient',
            'dentist',
            'branch',
            'visit',
            'treatment_title',
            'appointment',
            'insurance',
            'teeth_number',
            'medication',
            'closed',
            'notes',
        ]
