# Generated by Django 4.0.2 on 2022-02-23 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leaves', '0002_alter_leave_annual_total_leave'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leave',
            old_name='leavetype',
            new_name='leave_type',
        ),
    ]
