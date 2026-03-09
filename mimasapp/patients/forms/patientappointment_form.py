from django import forms

from patients.models.patients_model import Patient
from patients.models.patientinsurance_model import PatientInsurance
from patients.models.patientappointment_model import PatientAppointment, AppointmentStatus
from mimascompany.models.branch_model import Branch
from mimascompany.models.dentist_model import Dentist


# Patient appointment form
class PatientAppointmentForm(forms.ModelForm):

    # ---- Appointment info ----
    appointment_title = forms.CharField(label='Appointment Title')
    reason = forms.CharField(label='Reason')
    appointment_date = forms.DateField(
        label='Appointment Date',
        widget= forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})
    )
    appointment_time = forms.ChoiceField(
        label='Appointment Time',
        choices=PatientAppointment.APPOINT_TIME
    )
    status = forms.ChoiceField(
        label='Status',
        choices=AppointmentStatus.choices
    )

    # ---- Related models ----
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        label='Patient',
        widget=forms.Select()
    )
    dentist = forms.ModelChoiceField(
        label='Dentist',
        queryset=Dentist.objects.all(),
        widget=forms.Select()
    )
    branch = forms.ModelChoiceField(
        widget=forms.Select(),
        label='Branch',
        queryset=Branch.objects.all()
    )
    insurance = forms.ModelChoiceField(
        label='Insurance',
        required=False,
        queryset=PatientInsurance.objects.all(),
        widget=forms.Select(),
    )

    # ---- Appointment options ----
    number_appointments = forms.IntegerField(
        initial=1,
        min_value=1,
        widget=forms.NumberInput(),
        label='Number of Appointments',
    )
    frequency = forms.ChoiceField(
        label='Frequency',
        widget=forms.Select(),
        choices=[
            ('1', 'Weekly'),
            ('2', 'Bi-weekly'),
            ('4', 'Monthly')
        ]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ''
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'width: 400px'

    class Meta:
        model = PatientAppointment
        fields = [
            'patient',
            'dentist',
            'branch',
            'insurance',
            'status',
            'appointment_title',
            'appointment_date',
            'appointment_time',
            'reason'
        ]
        exclude = ['updated_by']
