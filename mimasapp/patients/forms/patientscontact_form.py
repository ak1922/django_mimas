from django import forms

from patients.models.patients_model import Patient
from patients.models.patientcontact_model import PatientContact


# Patient contact form
class PatientContactForm(forms.ModelForm):

    contact_name = forms.CharField(label='Contact Name')
    contact_address = forms.CharField(label='Contact Address')
    contact_phone = forms.CharField(label='Contact Phone')
    relationship = forms.CharField(label='Relationship')

    # ---- Related models ----
    patient = forms.ModelChoiceField(
        label='Patient',
        queryset=Patient.objects.all(),
        widget=forms.Select
    )

    # ---- Overrides and Filters ----
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.label_suffix = ''
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'width: 400px'

        existing_patient_contact_ids = PatientContact.objects.values_list('patient_id', flat=True)
        queryset = Patient.objects.exclude(id__in=existing_patient_contact_ids)

        if self.instance and self.instance.pk:
            current_patient = Patient.objects.filter(pk=self.instance.patient_id)
            self.fields['patient'].queryset = queryset | current_patient
        else:
            self.fields['patient'].queryset = queryset
            self.fields['patient'].empty_label = 'Select a Patient'

    class Meta:
        model = PatientContact
        fields = ['patient', 'contact_name', 'contact_address', 'contact_phone', 'relationship']
        exclude = ['updated_by']
