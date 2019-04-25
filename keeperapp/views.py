from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from keeperapp.forms import ProfileForm, UserForm, UserFormForEdit, CategoryForm, CategoryInfoForm, RecordForm
from keeperapp.models import CategoryInfo, Record


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
    info = CategoryInfo.objects.filter(category__user__username=request.user.username)
    return render(request, 'user/categories.html', {
        'info': info
    })


@login_required(login_url='/user/sign-in')
def edit_category(request, category_id):
    category_info = CategoryInfo.objects.get(id=category_id)
    category_form = CategoryForm(instance=category_info.category)
    category_info_form = CategoryInfoForm(instance=category_info)

    if request.method == "POST":
        category_form = CategoryForm(request.POST, instance=category_info.category)
        category_info_form = CategoryInfoForm(
            request.POST, request.FILES, instance=category_info
        )

    if category_form.is_valid() and category_info_form.is_valid():
        category_form.save()
        category_info_form.save()

    return render(request, 'user/edit_category.html', {
        'category_form': category_form,
        'category_info_form': category_info_form
    })


@login_required(login_url='/user/sign-in')
def add_category(request):
    category_form = CategoryForm()
    category_info_form = CategoryInfoForm()

    if request.method == "POST":
        category_form = CategoryForm(request.POST)
        category_info_form = CategoryInfoForm(request.POST, request.FILES)

        if category_form.is_valid() and category_info_form.is_valid():
            new_category = category_form.save(commit=False)
            new_category.user = request.user
            new_category.save()
            new_category_info = category_info_form.save(commit=False)
            new_category_info.category = new_category
            new_category_info.save()
            return redirect(user_categories)

    return render(request, 'user/add_category.html', {
        'category_form': category_form,
        'category_info_form': category_info_form
    })


@login_required(login_url='/user/sign-in')
def user_records(request):
    info = CategoryInfo.objects.filter(category__user__username=request.user.username)
    return render(request, 'user/records.html', {
        'information': info
    })


@login_required(login_url='/user/sign-in')
def add_record(request):
    record_form = RecordForm()

    if request.method == 'POST':
        record_form = RecordForm(request.POST, request.FILES)
        if record_form.is_valid():
            new_record = record_form.save(commit=False)
            new_record.user = request.user
            new_record.save()
            return redirect(user_record_info, new_record.category.id)

    return render(request, 'user/add_record.html', {
        'record_form': record_form
    })


@login_required(login_url='/user/sign-in')
def user_record_info(request, category_id):
    if Record.objects.filter(category__id=category_id).count() == 0:
        return redirect(add_record)

    records = Record.objects.filter(
        category__user__username=request.user.username, category__id=category_id)

    return render(request, 'user/record_info.html', {
        'records': records,
        'category_name': records[0].category.name
    })
