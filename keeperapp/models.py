from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from jsonfield import JSONField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=500)
    state = models.CharField(max_length=500)
    zip = models.CharField(max_length=500)
    avatar = models.ImageField(upload_to='profile_avatar/',
                               blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return "/static/img/default-profile-icon-24.jpg"

    def __str__(self):
        return self.user.username


class Category(models.Model):
    # The columns field is a comma separated list of names that will populate the record headers
    # Example: Name, Cost, Date
    class Meta:
        verbose_name_plural = 'categories'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    columns = models.TextField(max_length=2000)
    options = JSONField(max_length=2000, default='{"null":"null"}')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CategoryInfo(models.Model):
    # This is the extended Category information.
    # TODO: Combine CategoryInfo & Category
    class Meta:
        verbose_name_plural = 'CategoryInfo'

    category = models.OneToOneField(
        Category,
        on_delete=models.CASCADE,
        related_name='category_data',
        default=1
    )
    description = models.TextField(max_length=2000)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    file = models.FileField(upload_to='files/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return "/static/img/699086-icon-94-folder-512.png"

    def __str__(self):
        return str(self.id)


class Option(models.Model):
    # This model is unused. It's a placeholder for themes, and various options
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_options')
    view = models.CharField(max_length=500)
    theme = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Record(models.Model):
    # The data field is composed of JSON and uses the Category.columns as Key names
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='record_user')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='record_category'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    data = JSONField(max_length=2000)
    date = models.DateTimeField(blank=True, null=True, default=timezone.now)
    file = models.FileField(upload_to='files/', blank=True)

    def __str__(self):
        return str(self.id)
