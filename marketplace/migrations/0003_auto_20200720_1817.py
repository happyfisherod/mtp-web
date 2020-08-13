# Generated by Django 3.0.3 on 2020-07-20 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0002_auto_20200720_1143'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobapply',
            old_name='name',
            new_name='subject',
        ),
        migrations.RenameField(
            model_name='workerhire',
            old_name='name',
            new_name='subject',
        ),
        migrations.RemoveField(
            model_name='jobapply',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='jobapply',
            name='website',
        ),
        migrations.RemoveField(
            model_name='workerhire',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='workerhire',
            name='website',
        ),
    ]
