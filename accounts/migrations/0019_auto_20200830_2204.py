# Generated by Django 3.0.3 on 2020-08-30 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_auto_20200815_0031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='mapillary_access_token',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
