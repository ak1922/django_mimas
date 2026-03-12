from django import forms

from mimascompany.models import Branch, Dentist
from dentists.models.dentistreport_model import DentistReport
from patients.models import Patient, PatientVisit, PatientAppointment, PatientInsurance


# Dentist report form
class DentistReportForm(forms.ModelForm):

    required_css_class = 'required'

    report_title = forms.CharField(label='Report Title')
    closed = forms.BooleanField(
        label='Closed',
        widget=forms.CheckboxInput(),
        required=False
    )
    history = forms.CharField(
        label='History',
        required=False,
        widget=forms.Textarea(
            attrs={'rows': 3, 'cols': 20}
        )
    )
    clinical_finding = forms.CharField(
        required=False,
        label='Clinical Finding',
        widget=forms.Textarea(
            attrs={'rows': 3, 'cols': 20,}
        )
    )
    diagnosis = forms.CharField(
        label='Diagnosis',
        required=False,
        widget=forms.Textarea(
            attrs={'rows': 3, 'cols': 20,}
        )
    )
    general_comments = forms.CharField(
        label='General Comments',
        widget=forms.Textarea(
            attrs={'rows': 3, 'cols': 20,}
        ),
        required=False
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
        model = DentistReport
        exclude = ['updated_by']
        fields = [
            'patient',
            'dentist',
            'branch',
            'visit',
            'report_title',
            'appointment',
            'insurance',
            'history',
            'clinical_finding',
            'diagnosis',
            'closed',
            'general_comments'
        ]
