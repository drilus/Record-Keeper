# Generated by Django 2.2 on 2019-04-23 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('keeperapp', '0003_auto_20190422_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorydata',
            name='category',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='category_data', to='keeperapp.Category'),
        ),
        migrations.AlterField(
            model_name='categorydata',
            name='description',
            field=models.TextField(max_length=2000),
        ),
    ]
