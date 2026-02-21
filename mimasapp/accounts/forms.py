from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from .models import AccountUser


# Register user form
class RegisterAppUserForm(forms.ModelForm):
    """ Registration form for all app users employees, dentists and patients """

    # Password fields
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'style': 'width: 400px',
                'class': 'form-control'
            }
        )
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                'style': 'width: 400px',
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = AccountUser
        fields = ['username', 'email', 'user_type']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 400px'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'style': 'width: 400px'}),
            'user_type': forms.Select(attrs={'class': 'form-control', 'style': 'width: 400px'})
        }

    def clean_email(self):
        """ Validate provided email """

        email = self.cleaned_data.get('email')
        if AccountUser.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def clean_username(self):
        """ Validate provided username """

        username = self.cleaned_data.get('username')
        if AccountUser.objects.filter(username=username).exists():
            raise ValidationError("This username provided is already taken. Use another name or add numbers to the current username.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        # 3. Check for matching passwords
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")

        # Validate password strength (optional but recommended)
        # if password1:
        #     validate_password(password1)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# User login form
class AppLoginForm(forms.Form):

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'style': 'width: 400px'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'style': 'width: 400px'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            # We don't authenticate here, just check if email exists if needed
            # Or leave clean empty and handle error in view
            pass
        return cleaned_data

    class Meta:
        model = AccountUser
        fields = ['email', 'password']