# Generated by Django 3.0.3 on 2020-07-27 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0018_auto_20200727_0858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
