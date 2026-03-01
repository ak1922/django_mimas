from django import forms

from patients.models.patients_model import Patient
from patients.models.patientinsurance_model import PatientInsurance


# Patient insurance form
class PatientInsuranceForm(forms.ModelForm):

    company = forms.CharField(label='Company')
    policy_number = forms.CharField(label='Policy Number')
    group_name = forms.CharField(label='Group Name')
    group_number = forms.CharField(label='Group Number')
    company_phone = forms.CharField(label='Company Phone')
    subscriber_name = forms.CharField(label='Subscriber Name')
    subscriber_dob = forms.CharField(
        label='Subscriber DOB',
        widget= forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})
    )
    subscriber_relation_patient = forms.CharField(label='Subscriber Patient Relationship')

    # ---- Related models ----
    patient = forms.ModelChoiceField(
        label='Patient',
        queryset=Patient.objects.all(),
        widget=forms.Select()
    )

    # ---- Filters & Overrides ----
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.label_suffix = ''
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'width: 400px'

        existing_insurance_patient_ids = PatientInsurance.objects.values_list('patient_id', flat=True)
        queryset = Patient.objects.exclude(patient_id__in=existing_insurance_patient_ids)

        if self.instance and self.instance.pk:
            current_patient = Patient.objects.filter(pk=self.instance.patient_id)
            self.fields['patient'].queryset = queryset | current_patient
        else:
            self.fields['patient'].queryset = queryset
            self.fields['patient'].empty_label = 'Select a Patient'

    class Meta:
        model = PatientInsurance
        fields = '__all__'
        exclude = ['updated_by']
