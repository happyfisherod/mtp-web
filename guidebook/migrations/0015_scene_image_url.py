# Generated by Django 3.0.3 on 2020-08-06 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guidebook', '0014_auto_20200804_1322'),
    ]

    operations = [
        migrations.AddField(
            model_name='scene',
            name='image_url',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
