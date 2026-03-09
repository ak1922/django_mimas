from django import forms
from django.db.models import Q

from accounts.models import AccountUser, UserType
from mimascompany.models.employee_model import CompanyPositions, Employee


# Positions form
class CompanyPositionForm(forms.ModelForm):

    required_css_class = 'required'

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

    required_css_class = 'required'

    # ---- Personal info
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    gender = forms.ChoiceField(choices=Employee.GENDER_CHOICES)
    status = forms.ChoiceField(choices=Employee.EmployeeStatus.choices)

    # ---- ForignKey fields -----
    user = forms.ModelChoiceField(queryset=AccountUser.objects.all())
    position = forms.ModelChoiceField(queryset=CompanyPositions.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ''
            field.widget.attrs['style'] = 'width: 400px'
            field.widget.attrs['class'] = 'form-control'

        eligible_users = AccountUser.objects.filter(
            Q(user_type=UserType.EMPLOYEES) |
            Q(user_type=UserType.DENTISTS) |
            Q(user_type=UserType.ADMINISTRATORS)
        ).distinct()

        if self.instance and self.instance.pk:
            self.fields['user'].queryset = AccountUser.objects.filter(
                Q(user_type=UserType.EMPLOYEES) |
                Q(user_type=UserType.DENTISTS) |
                Q(user_type=UserType.ADMINISTRATORS)
            ).distinct()
        else:
            self.fields['user'].queryset = eligible_users.filter(
                employee_accountuser__isnull=True
            )

    class Meta:
        model = Employee
        fields = ['user', 'first_name', 'last_name', 'gender', 'photo', 'position', 'status']
        exclude = ['updated_by', 'vacations_days_accrued']


# Upload photo form
class UploadImageForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ['photo']
        exclude = ['first_name', 'last_name', 'gender', 'status', 'user', 'position']
