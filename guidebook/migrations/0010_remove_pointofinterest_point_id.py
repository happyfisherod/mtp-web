# Generated by Django 3.0.3 on 2020-08-02 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guidebook', '0009_auto_20200802_1236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pointofinterest',
            name='point_id',
        ),
    ]
