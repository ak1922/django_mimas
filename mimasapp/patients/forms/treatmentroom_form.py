from django import forms

from mimascompany.models.branch_model import Branch
from patients.models.treatmentroom_model import TreatmentRoom
from patients.models.patientvisit_models import PatientVisit


# Treatment room form
class TreatmentRoomForm(forms.ModelForm):

    room_name = forms.CharField(label='Room Name')
    # room_number = forms.IntegerField(
    #     label='Room Number',
    #     required=False
    # )
    is_occupied = forms.CharField(
        label='Is Occupied',
        required=False,
        widget=forms.CheckboxInput()
    )

    # ---- Related models ----
    visit = forms.ModelChoiceField(
        label='Patient Visit',
        queryset=PatientVisit.objects.all(),
        widget=forms.Select(),
        required=False
    )
    branch = forms.ModelChoiceField(
        label='Branch',
        queryset=Branch.objects.all(),
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
        model = TreatmentRoom
        exclude = ['updated_by']
        fields = [
            'room_name',
            'visit',
            'branch'
        ]
