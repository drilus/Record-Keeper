# Generated by Django 2.2 on 2019-05-17 03:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('keeperapp', '0017_auto_20190510_0236'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='categoryinfo',
            name='category',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='category_data', to='keeperapp.Category'),
        ),
    ]
