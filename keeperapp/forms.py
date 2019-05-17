from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from keeperapp.models import Profile, Category, CategoryInfo, Record
from jsonfield import JSONField


class UserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            'username',
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


class AddRecordForm(forms.ModelForm):
    file = forms.FileField(required=False)
    data = JSONField()

    class Meta:
        model = Record
        widgets = {
            'data': forms.HiddenInput(),
            'date': forms.DateTimeInput(attrs={'class': 'datetime-input'})
        }
        fields = (
            'category',
            'data',
            'file',
            'date'
        )

    # Only pull category objects that are created by the user
    # Default uses Category.objects.all()
    def __init__(self, user, *args, **kwargs):
        super(AddRecordForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)


class RecordForm(forms.ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = Record
        fields = (
            'category',
            'data',
            'date',
            'file'
        )
        widgets = {
            'date': forms.DateTimeInput(attrs={'class': 'datetime-input'})
        }

    # Only pull category objects that are created by the user
    # Default uses Category.objects.all()
    def __init__(self, user, *args, **kwargs):
        super(RecordForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)


class RecordColumnForm(forms.Form):

    def __init__(self, user, *args, **kwargs):
        super(RecordColumnForm, self).__init__(*args, **kwargs)
        names = Category.objects.filter(user=user)
        for name in names:
            columns = name.columns.split(',')
            for column in columns:
                self.fields['column_{}_{}'.format(name.id, column.strip())] = \
                    forms.CharField(label=column.strip(), required=False)
