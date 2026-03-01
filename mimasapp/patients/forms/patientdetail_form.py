from django import forms

from patients.models.patients_model import Patient
from patients.models.patientdetails_model import PatientDetail
from mimascompany.models.dentist_model import Dentist


# Patient detail form
class PatientDetailForm(forms.ModelForm):

    # -------------------------------------
    ssn = forms.CharField(label='SSN')
    phone_number = forms.CharField(label='Phone Number')
    address = forms.CharField(label='Address')
    date_of_birth = forms.DateField(
        label='Date of Birth',
        widget= forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})
    )
    # -------------------------------------
    weight = forms.DecimalField(
        required=False,
        label='Weight'
    )
    height = forms.DecimalField(
        label='Height',
        required=False
    )
    allergies = forms.CharField(
        label='Allergies',
        required=False
    )
    blood_type = forms.ChoiceField(
        label='Blood Type',
        required=False,
        choices=PatientDetail.BlodType.choices
    )
    current_medication = forms.CharField(
        required=False,
        label='Current Medication'
    )

    # ---- Related models ----
    patient = forms.ModelChoiceField(
        label='Patient',
        queryset=Patient.objects.all(),
        widget=forms.Select()
    )
    secondary_dentist = forms.ModelMultipleChoiceField(
        label='Secondary Dentist',
        required=False,
        queryset=Dentist.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )

    # ---- Filters & Overrides ---------
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.label_suffix = ''

            if not isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['style'] = 'width: 400px'


        if self.instance and self.instance.pk and hasattr(self.instance, 'patient'):
            try:
                primary_dentist = self.instance.patient.primary_dentist
                if primary_dentist:
                    self.fields['secondary_dentist'].queryset = Dentist.objects.exclude(pk=primary_dentist.pk)
            except Patient.DoesNotExist:
                pass

        existing_details_patient_ids = PatientDetail.objects.values_list('patient_id', flat=True)
        queryset = Patient.objects.exclude(patient_id__in=existing_details_patient_ids)

        if self.instance and self.instance.pk:
            current_patient = Patient.objects.filter(pk=self.instance.patient_id)
            self.fields['patient'].queryset = queryset | current_patient
        else:
            self.fields['patient'].queryset = queryset

        self.fields['patient'].empty_label = 'Select a Patient'

    class Meta:
        model = PatientDetail
        fields = [
            'patient',
            'ssn',
            'date_of_birth',
            'phone_number',
            'address',
            'blood_type',
            'allergies',
            'height',
            'weight',
            'current_medication',
            'secondary_dentist'
        ]
        exclude = ['updated_by']


# Patient detail read only form
class PatientDetailReadOnlyForm(forms.ModelForm):
    class Meta:
        model = PatientDetail
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PatientDetailReadOnlyForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label_suffix = ''

            if not isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['style'] = 'width: 400px'