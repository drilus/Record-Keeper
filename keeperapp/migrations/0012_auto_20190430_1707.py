# Generated by Django 2.2 on 2019-04-30 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keeperapp', '0011_auto_20190427_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='static/img/default-profile-icon-24.jpg', upload_to='profile_avatar/'),
        ),
    ]
