# Generated by Django 3.0.3 on 2020-07-29 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0025_auto_20200727_1811'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='imagequality',
            options={'verbose_name_plural': 'Image Quality'},
        ),
        migrations.AlterModelOptions(
            name='organisationcategory',
            options={'verbose_name_plural': 'Organisation Categories'},
        ),
    ]
