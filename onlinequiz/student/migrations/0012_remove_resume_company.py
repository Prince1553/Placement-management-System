# Generated by Django 4.1.7 on 2023-05-10 07:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0011_resume_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resume',
            name='company',
        ),
    ]
