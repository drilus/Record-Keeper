from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.db.models import Count
from django.http import HttpResponse

from keeperapp.forms import ProfileForm, UserFormForEdit, CategoryForm, CategoryInfoForm, \
    RecordForm, UserCreationForm, RecordColumnForm, AddRecordForm
from keeperapp.models import CategoryInfo, Record, Category
from keeperapp.serializers import CategorySerializer
import datetime
import csv


def home(request):
    return redirect(user_home)


@login_required(login_url='/user/sign-in')
def user_home(request):
    return redirect(user_overview)


def user_sign_up(request):
    # TODO: Check for username availability -- will probably need to be a separate API request
    user_creation_form = UserCreationForm()
    profile_form = ProfileForm()

    if request.method == 'POST':
        user_creation_form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_creation_form.is_valid() and profile_form.is_valid():
            new_user = User.objects.create_user(
                username=user_creation_form.cleaned_data['username'],
                email=user_creation_form.cleaned_data['email'],
                password=user_creation_form.cleaned_data['password1'],
                first_name=user_creation_form.cleaned_data['first_name'],
                last_name=user_creation_form.cleaned_data['last_name']
            )
            new_profile = profile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()

            login(request, authenticate(
                username=user_creation_form.cleaned_data['username'],
                password=user_creation_form.cleaned_data['password1']
            ))

            return redirect(user_home)

    return render(request, 'user/sign_up.html', {
        'user_form': user_creation_form,
        'profile_form': profile_form
    })


@login_required(login_url='/user/sign-in')
def user_overview(request):
    # Only pull categories that have a 'cost' field
    categories = Category.objects.filter(user=request.user, columns__icontains='cost')

    # calculate total for each category with a "cost" field
    # also round to two decimal places
    total_per_category = []
    for category in categories:
        cost = round(sum(float(record.data['Cost']) for record in Record.objects.filter(
            user=request.user, category__id=category.id
        )), 2)
        # total_per_category.append('${0:,.2f}'.format(cost))
        total_per_category.append(cost)

    # count total records per category
    record_count = Category.objects.filter(user=request.user).annotate(
        num_records=Count('record_category')
    ).order_by('-num_records')

    # ChartJS uses 'labels' and 'data' arrays to display graph's
    records_per_category = {
        'labels': [cat.name for cat in record_count],
        'data': [rec.num_records for rec in record_count]
    }

    spending = {
        'labels': [category.name for category in categories],
        'data': total_per_category
    }

    return render(request, 'user/overview.html', {
        'spending': spending,
        'records_per_category': records_per_category
    })


@login_required(login_url='/user/sign-in')
def user_settings(request):
    # Allow the user to change their profile information
    # This view can be extended to use the future Options model
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
    category_info = CategoryInfo.objects.get(category__id=category_id)
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
        return redirect(user_categories)

    return render(request, 'user/edit_category.html', {
        'category_form': category_form,
        'category_info_form': category_info_form
    })


@login_required(login_url='/user/sign-in')
def add_category(request):
    # We are passing the Category & CategoryInfo models to a form.
    # TODO: Refactor: Combine Category & CategoryInfo models
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
    record_form = AddRecordForm(request.user)
    record_columns = RecordColumnForm(request.user)

    # Need to pass category object through a serializer to return JSON
    category_names = CategorySerializer(
        Category.objects.filter(user=request.user),
        many=True,
        context={"request": request}
    ).data

    # Don't save the record object until after we assign the user
    if request.method == 'POST':
        record_form = RecordForm(request.user, request.POST, request.FILES)
        if record_form.is_valid():
            new_record = record_form.save(commit=False)
            new_record.user = request.user
            new_record.save()
            return redirect(user_category_records, new_record.category.id)

    # We need to pass the Form data and the category column data to use in record headers.
    return render(request, 'user/add_record.html', {
        'record_form': record_form,
        'record_columns': record_columns,
        'category_names': category_names
    })


@login_required(login_url='/user/sign-in')
def user_category_records(request, category_id):
    # Redirect user to add a record if no records exist
    if Record.objects.filter(category__id=category_id).count() == 0:
        return redirect(add_record)

    records = Record.objects.filter(
        category__user__username=request.user.username, category__id=category_id)

    # {
    #   "sort_by": {
    #     "column": {
    #       "name": "Date",
    #       "descending": true
    #     },
    #     "format": "%Y/%m/%d"
    #   }
    # }
    # TODO: Need a better method for sorting data
    options = records[0].category.options
    if 'sort_by' in options.keys():
        descending = options['sort_by']['column']['descending']
        column = options['sort_by']['column']['name']
        format = options['sort_by']['format']
        records = sorted(records, key=lambda x: datetime.datetime.strptime(
            x.data[column], format).date(), reverse=descending)

    # Get columns to use as table headers
    columns = list(map(lambda x: x.strip(), Category.objects.get(id=category_id).columns.split(',')))

    # TODO: Move this request to Options view
    # Export our record data into CSV format
    if request.method == 'POST':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'

        columns.append('Date')
        writer = csv.DictWriter(response, fieldnames=columns)
        writer.writeheader()
        for record in records:
            record.data['Date'] = str(record.date)
            writer.writerow(record.data)
        return response

    return render(request, 'user/record_info.html', {
        'records': records,
        'category_name': records[0].category.name,
        'columns': columns
    })


@login_required(login_url='/user/sign-in')
def edit_record(request, record_id):
    # Grab the record using it's internal id. Pass the record object to a form
    record = Record.objects.get(id=record_id)
    record_form = RecordForm(request.user, instance=record)

    if request.method == "POST":
        record_form = RecordForm(
            request.user, request.POST, request.FILES, instance=record
        )

    if record_form.is_valid():
        record_form.save()
        return redirect(user_category_records, record.category.id)

    return render(request, 'user/edit_record.html', {
        'record_form': record_form
    })
