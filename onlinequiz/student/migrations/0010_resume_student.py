# Generated by Django 4.1.7 on 2023-05-09 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0009_remove_resume_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='student',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='student.student'),
            preserve_default=False,
        ),
    ]
