from django import forms
from django.contrib.auth.models import User
from keeperapp.models import Profile, Category, CategoryInfo, Record


class UserForm(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'first_name',
            'last_name',
            'email'
        )


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


class UserFormForEdit(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email"
        )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
            'name',
            'columns',
            'options'
        )


class CategoryInfoForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    file = forms.FileField(required=False)

    class Meta:
        model = CategoryInfo
        fields = (
            'description',
            'image',
            'file'
        )


class RecordForm(forms.ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = Record
        fields = (
            'category',
            'data',
            'file'
        )
