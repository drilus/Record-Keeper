from django.contrib import admin

from keeperapp.models import Profile, Category, CategoryData, Option, Record

# Register your models here.
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(CategoryData)
admin.site.register(Option)
admin.site.register(Record)
