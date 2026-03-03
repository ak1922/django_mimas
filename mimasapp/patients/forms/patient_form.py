from django import forms

from accounts.models import AccountUser
from mimascompany.models.dentist_model import Dentist
from mimascompany.models.employee_model import Employee
from patients.models.patients_model import Patient


# Patient form
class PatientForm(forms.ModelForm):

    # ---- Patients Info ----
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            format='%Y-%m-%d', attrs={'type': 'date'}
        )
    )
    gender = forms.ChoiceField(
        label='Gender',
        choices=Patient.Gender.choices
    )

    # ---- ForeignKey fields -----
    patient = forms.ModelChoiceField(
        label='Patient',
        queryset=AccountUser.objects.all()
    )
    primary_dentist = forms.ModelChoiceField(
        label='Dentist',
        queryset=Dentist.objects.all()
    )

    # ---- Filters & Overrides ----
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.label_suffix = ''
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'width: 400px'

        existing_patient = Patient.objects.values_list('patient_id', flat=True)
        self.fields['patient'].queryset = AccountUser.objects.filter(
            user_type='Patients'
        ).exclude(id__in=existing_patient)

        if self.instance and self.instance.patient_id:
            self.fields['patient'].queryset = AccountUser.objects.filter(id=self.instance.patient_id)

    class Meta:
        model = Patient
        fields = ['patient', 'first_name', 'last_name', 'date_of_birth', 'gender', 'primary_dentist']
        exclude = ['updated_by']


# Patient read only form
class PatientReadOnlyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.label_suffix = ''
            field.widget.attrs['style'] = 'width: 400px'
            field.widget.attrs['readonly'] = 'readonly'
            field.widget.attrs['class'] = 'readonly-field, form-control'

    class Meta:
        model = Patient
        fields = '__all__'
        exclude = ['created', 'updated']
