from django import forms

from mimascompany.models.employee_model import Employee
from mimascompany.models.employeecontact_model import EmployeeContact


# Employee contact form
class EmployeeContactForm(forms.ModelForm):

    required_css_class = 'required'

    # ---- Contact info ----
    contact_name = forms.CharField(label='Contact Name')
    contact_address = forms.CharField(label='Contact Address')
    contact_phone = forms.CharField(label='Contact Phone')
    relationship = forms.CharField(label='Relationship')

    # ---- Employee info ----
    employee = forms.ModelChoiceField(
        label='Employee',
        empty_label='Choose Employee',
        queryset=Employee.objects.all()
    )

    # ---- Overrides & Filters ----
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.label_suffix = ''
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'width: 400px'

        existing_contact = EmployeeContact.objects.values_list('employee_id', flat=True)
        without_contact = Employee.objects.exclude(user_id__in=existing_contact)

        if self.instance and self.instance.pk:
            self.fields['employee'].queryset = without_contact | Employee.objects.filter(pk=self.instance.employee_id)
        else:
            self.fields['employee'].queryset = without_contact
            self.fields['employee'].empty_label = 'Select an Employee'

    class Meta:
        model = EmployeeContact
        fields = [
            'employee',
            'contact_name',
            'contact_phone',
            'contact_address',
            'relationship'
        ]
        exclude = ['updated_by']
