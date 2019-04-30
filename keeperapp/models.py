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
    avatar = models.ImageField(upload_to='profile_avatar/',
                               blank=True,
                               default='static/img/default-profile-icon-24.jpg')

    def __str__(self):
        return self.user.username


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'categories'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    columns = models.TextField(max_length=2000)
    options = JSONField(max_length=2000, default='{}')

    def __str__(self):
        return self.name


class CategoryInfo(models.Model):
    class Meta:
        verbose_name_plural = 'CategoryInfo'

    category = models.OneToOneField(
        Category,
        on_delete=models.CASCADE,
        related_name='category_data',
        default='unknown'
    )
    description = models.TextField(max_length=2000)
    image = models.ImageField(upload_to='images/', blank=True)
    file = models.FileField(upload_to='files/', blank=True)

    def __str__(self):
        return str(self.id)


class Option(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_options')
    view = models.CharField(max_length=500)
    theme = models.CharField(max_length=500)

    def __str__(self):
        return self.user.username


class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='record_user')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='record_category'
    )
    data = JSONField(max_length=2000)
    file = models.FileField(upload_to='files/', blank=True)

    def __str__(self):
        return str(self.id)
