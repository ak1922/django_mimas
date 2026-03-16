from django import forms

from patients.models.archivedtreatment_model import ArchivedPatientTreatment
from patients.models.archivedlab_model import ArchivedPatientLab
from patients.models.archivedreferral_model import ArchivedPatientReferral
from dentists.models.archivedreport_model import ArchivedDentistReport

class ArchivedPatientTreatmentForm(forms.ModelForm):

    closed = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input'}
        )
    )

    class Meta:
        model = ArchivedPatientTreatment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ArchivedPatientTreatmentForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label_suffix = ''

            if field_name != 'closed':
                field.widget.attrs['readonly'] = 'readonly'
                # Ensure form-control class is set for other fields
                if 'class' in field.widget.attrs:
                    field.widget.attrs['class'] += ' readonly-field, form-control'
                else:
                    field.widget.attrs['class'] = 'readonly-field, form-control'
                    field.widget.attrs['style'] = 'width: 400px'
            else:
                field.widget.attrs['disabled'] = 'disabled'


# Archived Patient lab form
class ArchivedPatientLabForm(forms.ModelForm):

    closed = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input'}
        )
    )

    class Meta:
        model = ArchivedPatientLab
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ArchivedPatientLabForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label_suffix = ''

            if field_name != 'closed':
                field.widget.attrs['readonly'] = 'readonly'
                if 'class' in field.widget.attrs:
                    field.widget.attrs['class'] += ' readonly-field, form-control'
                else:
                    field.widget.attrs['class'] = 'readonly-field, form-control'
                    field.widget.attrs['style'] = 'width: 400px'
            else:
                field.widget.attrs['disabled'] = 'disabled'


# Archived referrals
class ArchivedPatientReferralForm(forms.ModelForm):

    closed = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input'}
        )
    )

    class Meta:
        model = ArchivedPatientReferral
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ArchivedPatientReferralForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label_suffix = ''

            if field_name != 'closed':
                field.widget.attrs['readonly'] = 'readonly'
                if 'class' in field.widget.attrs:
                    field.widget.attrs['class'] += ' readonly-field, form-control'
                else:
                    field.widget.attrs['class'] = 'readonly-field, form-control'
                    field.widget.attrs['style'] = 'width: 400px'
            else:
                pass

class ArchivedDentistReportForm(forms.ModelForm):

    closed = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)

    class Meta:
        model = ArchivedDentistReport
        fields = '__all__'
        exclude = ['modified_by']

    def __init__(self, *args, **kwargs):
        super(ArchivedDentistReportForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label_suffix = ''
            field.disabled = True

            if field_name != 'closed':
                field.widget.attrs['readonly'] = 'readonly'
                if 'class' in field.widget.attrs:
                    field.widget.attrs['class'] += ' readonly-field, form-control'
                else:
                    field.widget.attrs['class'] = 'readonly-field, form-control'
                    field.widget.attrs['style'] = 'width: 400px'
            else:
                pass
