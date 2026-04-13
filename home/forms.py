from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import UserProfile

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password2'):
            raise forms.ValidationError("Passwords don't match.")
        return cd.get('password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image']
        widgets = {
            'profile_image': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer',
                'accept': 'image/*'
            })
        }

class EmailChangeForm(forms.Form):
    password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput,
        help_text="Enter your password to confirm"
    )
    old_email = forms.EmailField(
        label="Current Email",
        help_text="Enter your current email address"
    )
    new_email = forms.EmailField(
        label="New Email"
    )
    new_email_confirm = forms.EmailField(
        label="Confirm New Email"
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self):
        """Save the new email to the user"""
        self.user.email = self.cleaned_data['new_email']
        self.user.save()
        return self.user

