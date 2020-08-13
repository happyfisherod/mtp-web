# Generated by Django 3.0.3 on 2020-07-22 20:38

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0011_auto_20200722_2038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='capture_method',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(default=1), size=None),
        ),
        migrations.AlterField(
            model_name='job',
            name='type',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(default=1), size=None),
        ),
    ]
