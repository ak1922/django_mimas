from django import forms

from mimascompany.models.branch_model import Branch
from mimascompany.models.dentist_model import Dentist
from mimascompany.models.employee_model import Employee


# Dentist form
class DentistForm(forms.ModelForm):

    specialty = forms.CharField(label='Specialty')

    employee = forms.ModelChoiceField(
        label='Employee',
        queryset=Employee.objects.all()
    )
    supervisor = forms.ModelChoiceField(
        label='Supervisor',
        queryset=Employee.objects.all()
    )
    branch_name = forms.ModelChoiceField(
        label='Branch Name',
        queryset=Branch.objects.all()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.label_suffix = ''
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'width: 400px'

        existing_dentist = Dentist.objects.values_list('employee_id', flat=True)
        incoming_dentist = Employee.objects.filter(
            dentist_employee__isnull=True
        ).exclude(pk__in=existing_dentist)

        if self.instance and self.instance.pk:
            self.fields['employee'].queryset = incoming_dentist | Employee.objects.filter(pk=self.instance.employee_id)
        else:
            self.fields['employee'].queryset = incoming_dentist
            self.fields['employee'].empty_label = 'Select an Employee'

    class Meta:
        model = Dentist
        fields = '__all__'
        exclude = ['updated_by']
