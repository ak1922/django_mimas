from django import forms
from django.db.models import Q

from accounts.models import UserType
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

        existing_dentist_ids = Dentist.objects.values_list('employee_id', flat=True)
        available_employees_qs = Employee.objects.filter(
            Q(dentist_employee__isnull=True),
            user__user_type=UserType.DENTISTS
        ).exclude(pk__in=existing_dentist_ids)

        if self.instance and self.instance.pk:
            current_employee = Employee.objects.filter(pk=self.instance.employee_id, user__user_type=UserType.DENTISTS)
            self.fields['employee'].queryset = available_employees_qs | current_employee
        else:
            self.fields['employee'].queryset = available_employees_qs

        self.fields['supervisor'].queryset = Employee.objects.filter(user__user_type=UserType.DENTISTS)

    class Meta:
        model = Dentist
        exclude = ['updated_by']
        fields = [
            'employee',
            'supervisor',
            'branch_name',
            'specialty'
        ]
