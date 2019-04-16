from django import forms
from django.contrib.auth.models import User
from keeperapp.models import Profile


class UserForm(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'phone',
            'address',
            'city',
            'state',
            'zip',
            'avatar'
        )
