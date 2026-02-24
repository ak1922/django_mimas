from django import forms

from accounts.models import AccountUser
from mimascompany.models.employee_model import CompanyPositions, Employee


# Positions form
class CompanyPositionForm(forms.ModelForm):

    title = forms.CharField(
        label='Title', label_suffix='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'style': 'width: 400px'
        })
    )
    description = forms.CharField(
        label='Description', label_suffix='',
        widget=forms.Textarea(attrs={
            'rows': 5, 'cols': 45,
            'class': 'form-control'
        })
    )

    class Meta:
        model = CompanyPositions
        exclude = ['updated_by']


# Employee form
class EmployeeForm(forms.ModelForm):

    # ---- Personal info
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    gender = forms.ChoiceField(choices=Employee.GENDER_CHOICES)
    status = forms.ChoiceField(choices=Employee.EmployeeStatus)

    # ---- ForignKey fields -----
    user = forms.ModelChoiceField(queryset=AccountUser.objects.all())
    position = forms.ModelChoiceField(queryset=CompanyPositions.objects.all())

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ''
            field.widget.attrs['style'] = 'width: 400px'
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Employee
        exclude = ['updated_by', 'vacations_days_accrued']


# Upload photo form
class UploadImageForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ['photo']
        exclude = ['first_name', 'last_name', 'gender', 'status', 'user', 'position']
