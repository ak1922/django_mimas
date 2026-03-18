from django import forms

from patients.models import (
    TreatmentRoom,
    ArchivedPatientBill,
    ArchivedPatientVisit,
    ArchivedPatientAppointment
)


# Treatment room read only form
class TreatmentRoomReadOnlyForm(forms.ModelForm):

    is_occupied = forms.CheckboxInput(attrs={'class': 'form-check-input'})

    class Meta:
        model = TreatmentRoom
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TreatmentRoomReadOnlyForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['readonly'] = 'readonly'
            field.widget.attrs['class'] = 'readonly-field, form-control'
            field.widget.attrs['style'] = 'width: 400px'
            field.label_suffix = ''


# Archived appointments
class ArchivedAppointmentsReadOnlyForm(forms.ModelForm):

    confirmed = forms.CheckboxInput(attrs={'class': 'form-check-input'})
    appointment_date = forms.DateField(
        label='Appointment Date',
        widget= forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})
    )

    class Meta:
        model = ArchivedPatientAppointment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ArchivedAppointmentsReadOnlyForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ''

            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['style'] = 'width: 400px'


# Archived visit form
class ArchivedPatientVisitReadOnlyForm(forms.ModelForm):

    class Meta:
        model = ArchivedPatientVisit
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ArchivedPatientVisitReadOnlyForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ''

            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['style'] = 'width: 400px'


# Archived bill form
class ArchivedPatientBillReadOnlyForm(forms.ModelForm):

    is_paid = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = ArchivedPatientBill
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ArchivedPatientBillReadOnlyForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ''

            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['style'] = 'width: 400px'
