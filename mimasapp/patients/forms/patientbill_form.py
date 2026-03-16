from django import forms

from patients.models import PatientBill, Patient, PatientAppointment, PatientVisit


# Patient bill form
class PatientBillForm(forms.ModelForm):

    bill_title = forms.CharField(label='Bill Title')
    total_charge = forms.DecimalField(
        label='Total Charge($)',
        widget=forms.TextInput()
    )
    is_paid = forms.BooleanField(
        label='Is Paid',
        required=False,
        widget=forms.CheckboxInput()
    )

    patient = forms.ModelChoiceField(
        label='Patient',
        queryset=Patient.objects.all(),
        widget=forms.Select()
    )
    appointment = forms.ModelChoiceField(
        label='Appointment Title',
        widget=forms.Select(),
        queryset=PatientAppointment.objects.all()
    )
    visit = forms.ModelChoiceField(
        label='Visit',
        queryset=PatientVisit.objects.all(),
        widget=forms.Select()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['total_charge'].initial = self.instance.totalcharge

        for field_name, field in self.fields.items():
            field.label_suffix = ''

            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['style'] = 'width: 400px'

    class Meta:
        model = PatientBill
        exclude = ['updated_by']
        fields = [
            'patient',
            'bill_title',
            'appointment',
            'visit',
            'is_paid'
        ]
