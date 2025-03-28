# Generated by Django 5.1.6 on 2025-03-06 08:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_delete_formresponse'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('standard', models.IntegerField()),
                ('subject', models.CharField(choices=[('Tamil', 'Tamil'), ('Maths', 'Maths')], max_length=10)),
                ('responses', models.JSONField()),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('assessment_status', models.CharField(default='Not Assessed', max_length=50)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.record')),
            ],
            options={
                'unique_together': {('student', 'standard', 'subject')},
            },
        ),
    ]
