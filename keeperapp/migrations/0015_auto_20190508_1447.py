# Generated by Django 2.2 on 2019-05-08 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('keeperapp', '0014_auto_20190508_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='profile_avatar/'),
        ),
    ]