from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from keeperapp.forms import ProfileForm, UserForm, UserFormForEdit


def home(request):
    return redirect(user_home)  # noqa: F821


@login_required(login_url='/user/sign-in')
def user_home(request):
    return render(request, 'user/overview.html', {})


def user_sign_up(request):
    user_form = UserForm()
    profile_form = ProfileForm()

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            new_user = User.objects.create_user(**user_form.cleaned_data)
            new_profile = profile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()

            login(request, authenticate(
                username=user_form.cleaned_data['username'],
                password=user_form.cleaned_data['password']
            ))

            return redirect(user_home)

    return render(request, 'user/sign_up.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required(login_url='/user/sign-in')
def user_overview(request):
    return render(request, 'user/overview.html', {})


@login_required(login_url='/user/sign-in')
def user_settings(request):
    user_form = UserFormForEdit(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)

    if request.method == "POST":
        user_form = UserFormForEdit(request.POST, instance=request.user)
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )

    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()

    return render(request, 'user/settings.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required(login_url='/user/sign-in')
def user_categories(request):
    return render(request, 'user/categories.html', {})


@login_required(login_url='/user/sign-in')
def user_records(request):
    return render(request, 'user/records.html', {})
