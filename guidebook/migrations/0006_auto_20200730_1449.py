# Generated by Django 3.0.3 on 2020-07-30 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('guidebook', '0005_auto_20200730_1420'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guidebook',
            name='category',
        ),
        migrations.AddField(
            model_name='guidebook',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='guidebook.Category'),
        ),
    ]
