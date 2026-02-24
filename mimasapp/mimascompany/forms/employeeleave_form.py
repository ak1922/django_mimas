from django import forms

from mimascompany.models.leaverequests_model import LeaveRequest


# Leave form
class LeaveRequestForm(forms.ModelForm):

    class Meta:
        model = LeaveRequest
        fields = ['employee', 'start_date', 'end_date', 'leave_type', 'reason']
        exclude = ['updated_by']
        widgets = {
            'start_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'end_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }

    def __init__(self, *args, **kwargs):
        super(LeaveRequestForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.label_suffix = ''
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['style'] = 'width: 400px'
