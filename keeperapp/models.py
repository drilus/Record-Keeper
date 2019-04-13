from django.db import models
from django.contrib.auth.models import User

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
