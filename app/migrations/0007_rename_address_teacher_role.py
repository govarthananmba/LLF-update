# Generated by Django 5.1.6 on 2025-02-28 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_district_state_block_school_district_state_teacher_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacher',
            old_name='address',
            new_name='role',
        ),
    ]
