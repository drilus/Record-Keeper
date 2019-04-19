from django.db import models
from django.contrib.auth.models import User

from jsonfield import JSONField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    state = models.CharField(max_length=500)
    zip = models.CharField(max_length=500)
    avatar = models.ImageField(upload_to='profile_avatar/', blank=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    columns = JSONField(max_length=2000)
    options = JSONField(max_length=2000)

    def __str__(self):
        return self.category


class CategoryData(models.Model):
    user = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    description = JSONField(max_length=2000)
    image = models.ImageField(upload_to='images/', blank=True)
    file = models.FileField(upload_to='files/', blank=True)

    def __str__(self):
        return self.name
