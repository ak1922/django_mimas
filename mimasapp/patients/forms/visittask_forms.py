from django import forms

from patients.models.visittask_model import PatientVisitTask
from patients.models.patientvisit_models import PatientVisit
from patients.models.patientappointment_model import PatientAppointment

# Employee task item
class PatientVisitTaskForm(forms.ModelForm):

    task_title = forms.CharField(label='Task Title')
    description = forms.CharField(
        label='Description',
        required=False,
        widget=forms.Textarea(
            attrs={'cols': 20, 'rows': 4}
        )
    )
    task_status = forms.ChoiceField(
        label='Task Status',
        choices=PatientVisitTask.STATUS_CHOICES,
        widget=forms.Select()
    )
    priority = forms.ChoiceField(
        label='Priority',
        choices=PatientVisitTask.Priority.choices,
        widget=forms.Select()
    )

    visit = forms.ModelChoiceField(
        label='Patient Visit',
        queryset=PatientVisit.objects.all(),
        widget=forms.Select()
    )
    appointment = forms.ModelChoiceField(
        label='Patient Appointment',
        queryset=PatientAppointment.objects.all(),
        widget=forms.Select(),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ''
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'width: 400px'

    class Meta:
        model = PatientVisitTask
        fields = [
            'task_title',
            'appointment',
            'visit',
            'task_status',
            'priority',
            'description',
        ]
