from django import forms
from django.db.models import Q

from mimascompany.models import Branch, Service, Dentist, Department
from patients.models import (
    Patient,
    PatientVisit,
    PatientInsurance,
    TreatmentRoom,
    PostVisitOption,
    PatientAppointment
)


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
        queryset=TreatmentRoom. treatments.is_available().all(),
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

        if self.instance and self.instance.pk:
            self.fields['treatment_room'].queryset = TreatmentRoom.objects.filter(
                Q(pk=self.instance.treatment_room_id) |
                Q(id__in=TreatmentRoom.treatments.is_available().values('id'))
            ).distinct()
        else:
            self.fields['treatment_room'].queryset = TreatmentRoom.treatments.is_available().all()

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
            'insurance',
            'treatment_room',
        ]
